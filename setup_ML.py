import pandas as pd
import numpy as np
import os
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from BPt import BPt_ML

def get_datafiles_df():
    
    df = pd.DataFrame()
    dr = os.path.join(os.getcwd(), 'data/abcd_structural/')
    modals = os.listdir(dr)

    for modal in modals:

        series = pd.Series()
        m_dr = os.path.join(dr, modal)
        files = os.listdir(m_dr)

        for file in files:
            subj = 'NDAR_' + file.replace('.npy', '')
            file_loc = os.path.join(m_dr, file)

            series[subj] = file_loc

        df[modal] = series

    df.index.name = 'src_subject_id'
    return df

def abs_mean(a):
    return np.mean(np.abs(a))

# Setup main ML object with logs
ML = BPt_ML(log_dr='setup_ML_Logs',
            existing_log='overwrite',
            verbose=True,
            random_state=5,
            notebook=False,
            mp_context='fork',
            n_jobs=32)

# Set default NaN values
ML.Set_Default_Load_Params(na_values=["Don't know", "Decline to answer", "Not sure"])

# Load saved targets df
targets_df = pd.read_csv('data/targets.csv', index_col='src_subject_id')

# Move family id to dif df
family_id_df = targets_df[['rel_family_id']]

# Drop from targets df
targets_df = targets_df.drop('rel_family_id', axis=1)

# Load the targets - with some outlier filtering, but just
# setting NaN if outlier.
ML.Load_Targets(df=targets_df,
                col_name=list(targets_df),
                data_type='a',
                filter_outlier_std=10,
                drop_na=False,
                drop_or_na='na',
                clear_existing=True)

# Show the distributions for all loaded Targets
ML.Show_Targets_Dist()

# Load family id as Strat
ML.Load_Strat(df=family_id_df,
              col_name='rel_family_id')

# Load the data files, apply different filtering
df = get_datafiles_df()
df.dropna(inplace=True)

ML.Load_Data_Files(df=df[['myelin', 'thick', 'sulc']],
                   load_func=np.load,
                   filter_outlier_std=10,
                   reduce_func=[np.std])

ML.Load_Data_Files(df=df[['curv']],
                   load_func=np.load,
                   filter_outlier_std=10,
                   reduce_func=[np.min, np.max, np.std])

# Save distribution videos
'''
for name, func in zip(['Mean', 'Abs. Mean', 'Min', 'Max', 'STD'],
                    [np.mean, abs_mean, np.min, np.max, np.std]):

    anim = ML.Show_Data_Dist(reduce_func=func, return_anim=True)
    plt.title(name)
    
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=2)

    save_loc = 'setup_ML_Logs/' + name + '.mp4'
    anim.save(save_loc, dpi=500, writer=writer)
'''

# Set to no test data
ML.Train_Test_Split(test_size=0)

# Set some verbosity params
ML.Set_Default_ML_Verbosity(pipeline_verbose=True,
                            best_params_score=True,
                            fold_name=True,
                            time_per_fold=True,
                            score_per_fold=True,
                            fold_sizes=True,
                            best_params=True)

# Save ML object
ML.Save('data/Base.ML', low_memory=True)
