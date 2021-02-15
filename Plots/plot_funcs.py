import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd
from IPython.display import display
from scipy.stats import linregress, theilslopes


def remove_duplicate_labels(ax):

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc=1)


def extract_scatter_points():

    xs = []
    ys = []

    ax = plt.gca()
    for cs in ax.collections:
        cs.set_offset_position('data')
        data = cs.get_offsets()[0]

        xs.append(data[0])
        ys.append(data[1])

    # Return as sorted
    xys = list(zip(xs, ys))
    xys_sorted = np.array(sorted(xys, key=lambda s: s[0]))
    xs = xys_sorted[:, 0]
    ys = xys_sorted[:, 1]

    return xs, ys

def check_powerlaw(xs, ys, trunc=None):

    if trunc is not None:
        xs = xs[trunc:]
        ys = ys[trunc:]

    r = linregress(np.log10(xs), np.log10(ys))
    plt.plot(np.log10(xs), r.slope*np.log10(xs) + r.intercept)
    plt.scatter(np.log10(xs), np.log10(ys))
    print('linregress slope:', r.slope, 'linregress rvalue:', r.rvalue)

    ts = theilslopes(np.log10(ys), np.log10(xs))
    print('Theil-Sen slope:', ts[0], '95% CI:', ts[2], ts[3])


def get_results(results_dr):

    results = {}
    incomplete_cnt = 0
    result_files = os.listdir(results_dr)

    for file in result_files:
        
        result = np.load(os.path.join(results_dr, file))
        name = file.replace('.npy', '')
        
        if len(file.split('---')) == 3:

            if len(result) > 1:
                results[name] = result
            else:
                incomplete_cnt += 1
                
        else:
            
            # Get correct name
            name = '---'.join(name.split('---')[:-1])
            
            if len(result) > 1:
                
                try:
                    results[name].append(result)
                except KeyError:
                    results[name] = [result]
                    
                # Once all 5 loaded, format correctly
                if len(results[name]) == 5:
                    
                    to_fill = results[name][0].copy()
                    to_fill[:,0] = np.mean(results[name], axis=0)[:,0]
                    to_fill[:,1] = np.std(results[name], axis=0)[:,0]
                    results[name] = to_fill

            else:
                incomplete_cnt += .2
            
    print('Found:', len(results), 'Incomplete:', incomplete_cnt)
            
    return results

def conv_to_df(results, only=None):
    
    parcels, models = [], []
    targets, scores = [], []
    stds, is_binary = [], []

    for result in results:

        split = result.split('---')
        
        # Restrict to only
        if only is not None:
            if split[0] not in only:
                continue
                
        # If chunked score, skip
        if isinstance(results[result], list):
            continue

        # Add to lists
        parcels.append(split[0])
        models.append(split[1])
        targets.append(split[2])
        score = results[result]
        
        # If regression
        if len(score) == 2:
            scores.append(score[0][0]) 
            stds.append(score[0][1])
            is_binary.append(False)

        # If binary
        else:
            scores.append(score[1][0])
            stds.append(score[1][1])
            is_binary.append(True)

    df = pd.DataFrame()
    df['parcel'] = parcels
    df['model'] = models
    df['is_binary'] = is_binary
    df['target'] = targets
    df['score'] = scores
    df['std'] = stds
    
    df = df.set_index(['model', 'parcel']).sort_index()
    
    return df

def plot_score_by_n(parc_sizes, scores, title, ylabel, xlim=1050,
                    log=False, ax=None, sm=1):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    
    cmap = plt.get_cmap('viridis')
    
    for parcel in scores.index:
        
        s = 100
                    
        if parcel.startswith('stacked_random_'):
            color = 'mediumblue'
            alpha = 1
            label = 'Stacked'
            marker = "+"
            s = 125

        elif parcel.startswith('voted_random_'):
            color = 'green'
            alpha = 1
            label = 'Voted'
            marker = "+"
            s = 125

        elif parcel.startswith('grid_random_'):
            color = 'purple'
            alpha = 1
            label = 'Grid'
            marker = "+"
            s = 125

        elif 'icosahedron' in parcel:
            color = cmap(0)
            alpha = 1
            label = 'Icosahedron'
            marker = 'p'

        elif 'random' in parcel:
            color = 'black'
            alpha = .5
            label = 'Random'
            marker = "+"
            
        elif 'freesurfer' in parcel:
            color = cmap(.4)
            alpha = 1
            label = 'Freesurfer Extracted'
            marker = "*"
        
        # Base
        else:

            alpha = .8

            if '_prob' in parcel:
                color = cmap(.9)
                label = 'Existing Prob'
                marker = "s"
            else:
                color = cmap(.7)
                label = 'Existing'
                marker = "o"

        n_parcels = parc_sizes[parcel]
        ax.scatter(n_parcels, scores.loc[parcel],
                    color=color, alpha=alpha,
                    label=label, marker=marker, s=s*sm)
        
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel('Num. Parcels', fontsize=16)
    
    if xlim is not None:
        ax.set_xlim(-10, xlim)

    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

    if log:
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    ax.legend()
    remove_duplicate_labels(ax)
    
    plt.title(title, fontsize=20)
    
def plot_scores(parc_sizes, means, ylabel, avg_only=False, model='average', **plot_args):

    if model == 'svm':
        plot_score_by_n(parc_sizes, means.loc[model], 'SVM', ylabel, xlim=None, **plot_args)
    if model == 'lgbm':
        plot_score_by_n(parc_sizes, means.loc[model], 'LGBM', ylabel, xlim=None, **plot_args)
    if model == 'elastic':
        plot_score_by_n(parc_sizes, means.loc[model], 'Elastic-Net', ylabel, xlim=None, **plot_args)
    else:
        plot_score_by_n(parc_sizes, means.groupby('parcel').mean(),
                        'All Model Pipelines Avg.', ylabel,
                        xlim=None, **plot_args)

def mean_score(df):
    return df['score'].mean()

def mean_rank(df):
    return df['rank'].mean()

def max_rank(df):
    return df['rank'].max()

def min_rank(df):
    return df['rank'].min()

def get_rank_order(df):
     
    # Sort so that best is at top
    df = df.sort_values('score', ascending=False)

    # Set ranks s.t., best has rank 1
    df['rank'] = np.arange(1, len(df)+1)

    return df['rank']

def get_rank_model_order(df):
    
    # Sort so that best is at top
    df = df.sort_values('score', ascending=False)
    
    # Set ranks s.t., best has rank 1
    df['rank'] = np.arange(1, len(df)+1)

    return df[['rank', 'model']]

def plot_ranks(parc_sizes, df, plot='mean',
               avg_only=False, **plot_args):
    
    parcel_df = df.reset_index().set_index('parcel')
    ranks = parcel_df.groupby(['model', 'target']).apply(get_rank_order)
    ranks = ranks.to_frame().reset_index()

    mean_ranks = ranks.groupby(['model', 'parcel']).apply(mean_rank)
    max_ranks = ranks.groupby(['model', 'parcel']).apply(max_rank)
    min_ranks = ranks.groupby(['model', 'parcel']).apply(min_rank)

    out_of = str(len(mean_ranks) // 3)
    post = ' - (' + out_of + ' Total)'

    if plot == 'max':
        plot_scores(parc_sizes, max_ranks,
                    ylabel='Max Rank' + post, avg_only=avg_only, **plot_args)
    elif plot == 'min':
        plot_scores(parc_sizes, min_ranks,
                    ylabel='Min Rank' + post, avg_only=avg_only, **plot_args)
    else:
        plot_scores(parc_sizes, mean_ranks,
                    ylabel='Mean Rank' + post, avg_only=avg_only, **plot_args)


def plot_rank_comparison(parc_sizes, df,
                         title='Mean Rank Across Model Pipeline',
                         xlim=None, **plot_args):

    

    parcel_df = df.reset_index().set_index('parcel')
    ranks = parcel_df.groupby(['target']).apply(get_rank_model_order)

    mean_ranks = ranks.groupby(['model', 'parcel']).apply(mean_rank)
    scores = mean_ranks.reset_index()

    plt.figure(figsize=(12, 8))
    cmap = plt.get_cmap('viridis')

    for ind in scores.index:
        
        s = 100
        marker = "o"
        alpha = .5
        
        score = scores.loc[ind, 0]
        model = scores.loc[ind, 'model']
        parcel = scores.loc[ind, 'parcel']
        
        if model == 'svm':
            color = cmap(.2)
            label = 'SVM'
        elif model == 'elastic':
            color = cmap(.5)
            label = 'Elastic-Net'
        else:
            color = cmap(.8)
            label = 'LGBM'
            
        n_parcels = parc_sizes[parcel]
        plt.scatter(n_parcels, score,
                    color=color, alpha=alpha,
                    label=label, marker=marker, s=s)
        
    plt.legend()
    remove_duplicate_labels()

    out_of = str(len(scores))
    plt.ylabel('Mean Rank - (' + out_of + ' Total)', fontsize=16)
    plt.xlabel('Num. Parcels', fontsize=16)
    
    if xlim is not None:
        plt.xlim(-10, xlim)
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    if log:
        plt.xscale('log')
        plt.yscale('log')
    
    plt.legend()
    remove_duplicate_labels()
    
    plt.title(title, fontsize=20)
    
def plot_raw_scores(parc_sizes, df, avg_only=False, log=False):
    
    split_means = df.groupby(['is_binary', 'model', 'parcel']).apply(mean_score)

    regression_means = split_means.loc[False]
    binary_means = split_means.loc[True]

    plot_scores(parc_sizes, regression_means,
                ylabel='Avg Explained Variance',
                avg_only=avg_only, log=log)
    plot_scores(parc_sizes, binary_means,
                ylabel='Avg ROC AUC',
                avg_only=avg_only, log=log)
    
def check_best(df, top_vals=[1, 3, 5, 10]):
    
    models_in_top = {t : [] for t in top_vals}

    for target in df.target.unique():

        top_x = df[df['target'] == target].sort_values('score', ascending=False).head(top_vals[-1])

        # Compute stats
        for i in top_vals:
            models = [top_x.index[j][0] for j in range(i)]
            models_in_top[i] += models

        display(top_x)

    for i in top_vals:

        sns.countplot(models_in_top[i])
        plt.title('Models in Top ' + str(i))
        plt.show()
        
def check_best_by_model(df, models=['elastic', 'svm', 'lgbm']):
    
    # Top specific to each model for each target
    for model in models:
        print('Model:', model)

        for target in df.target.unique():
            display(df[df['target'] == target].loc[model].sort_values('score', ascending=False).head(5))