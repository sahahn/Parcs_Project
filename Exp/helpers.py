import os
import numpy as np
import pandas as pd
import time
import random
import sys
import shutil

models = ['elastic', 'lgbm', 'svm']
split_if = ['stacked_random_', 'random_2000_']

def clean_cache(dr, scratch_dr):

    # Get results dr
    exp_dr = os.path.join(dr, 'Exp')
    results_dr = os.path.join(exp_dr, 'results')

    # Find total where means done
    total = int(len(models) * len(load_target_names(dr)))

    # Get the count of 100% parcellations
    parcs_counts = {}

    files = os.listdir(results_dr)
    for file in files:
        
        parc = file.split('---')[0]
        model = file.split('---')[1]
        
        # If this model is being considered
        if model in models:

            # Load the result, have to check if it's actually done
            result = np.load(os.path.join(results_dr, file))

            # If len is 4, then means this is just one repeat
            if len(file.split('---')) == 4:
                add = .2

            # Otherwise it is all 5
            else:
                add = 1
        
            if len(result) > 1:
                try:
                    parcs_counts[parc] += add
                except KeyError:
                    parcs_counts[parc] = add

    all_parc_keys = list(parcs_counts)
    random.shuffle(all_parc_keys)

    print('Checking for finished cached parcels!', flush=True)
    
    for end in ['' , '1', '2', '3', '4', '5']:
        dr = os.path.join(scratch_dr, 'cache' + end)
        if os.path.exists(dr):
            for parc in all_parc_keys:

                if parcs_counts[parc] == total:
                    cache_dr = os.path.join(dr, parc)
                    if os.path.exists(cache_dr):
                        print('DELETE:', cache_dr, flush=True)
                        shutil.rmtree(cache_dr, ignore_errors=True)

                else:
                    print('Parcel:', parc, parcs_counts[parc], '/', total)

def get_done(results_dr):

    # Check which jobs are done
    results = os.listdir(results_dr)
    done = set()

    for result in results:
        name = result.replace('.npy', '')

        try:
            r = np.load(os.path.join(results_dr, result))

        # If value error when loading,
        # means something is actively writing
        # so treat as done
        except ValueError:
            done.add(name)

            # Then skip rest of loop
            continue

        # If done add to done
        if len(r) > 1:
            done.add(name)

        # If started less than 30hr ago, treat as done
        elif time.time() - r < 108000:
            done.add(name)

    return done

def get_name(parcel, model, target, split=None):

    name = parcel + '---' + model + '---' + target

    if split is not None:
        name += '---' + str(split)

    return name

def load_target_names(dr):

    # Target names
    data_dr = os.path.join(dr, 'data')
    targets_loc = os.path.join(data_dr, 'targets.csv')
    targets = list(pd.read_csv(targets_loc,
                               index_col='src_subject_id',
                               nrows=0))
    targets.remove('rel_family_id') # Not a target

    return targets


def get_stacked_options():
    
    parcels = []

    for s in ['100', '200', '300']:
        for n in ['3', '5']:
            for r in ['0']:
                parcels += ['stacked_random_' + s + '_' + n + '_' + r]

    return parcels

def get_choice(dr):

    # Parcels
    parcel_dr = os.path.join(dr, 'parcels')
    parcels = [p.replace('.npy', '') for p in os.listdir(parcel_dr)]

    # Add extra stacking parcels if any to run
    parcels += get_stacked_options()

    # Load target names
    targets = load_target_names(dr)

    # Results Dr
    exp_dr = os.path.join(dr, 'Exp')
    results_dr = os.path.join(exp_dr, 'results')
    os.makedirs(results_dr, exist_ok=True)

    # Get done
    done = get_done(results_dr)

    # Generate list of all valid choices
    all_choices = []

    for parcel in parcels:
        
        # If this parcel gets splits
        if any([parcel.startswith(s) for s in split_if]):
            needs_split = True
        else:
            needs_split = False

        for model in models:
            for target in targets:

                # If doesn't need split, names are just one
                if not needs_split:
                    names = [get_name(parcel, model, target)]
                else:
                    names = [get_name(parcel, model, target, split=s) 
                             for s in range(5)]
                
                # Add to choices
                all_choices += names

    # Remove done from all choices
    all_choices = list(set(all_choices) - set(done))

    print('Remaining Choices:', len(all_choices), flush=True)

    # If non-negative
    if len(all_choices) > 0:

        # From all_choices, select one at random to return
        # this makes it less likely to submit two of the same job
        # accidently.
        name = random.choice(all_choices)
        
        parcel = name.split('---')[0]
        model = name.split('---')[1]
        target = name.split('---')[2]

        # If needs split
        if len(name.split('---')) == 4:
            split = name.split('---')[3]
        else:
            split = None
        
        # Generate save loc
        save_loc = os.path.join(results_dr, name + '.npy')

        print('Return pmt', parcel, model, target, split, flush=True)

        # Return this choice
        return parcel, model, target, split, save_loc

    # If done, return None's
    return None, None, None, None, None

def unpack_args():

    base = list(sys.argv)[1:]
    
    args = {'parcel': base[0],
            'model': base[1],
            'target': base[2],
            'split': base[3],
            'save_loc': base[4],
            'memory': int(float(base[5])),
            'partition': base[6],
            'cores': int(float(base[7])),
            'scale': int(float(base[8]))}

    # Proc split - if int or None
    try:
        args['split'] = int(float(args['split']))
    except ValueError:
        args['split'] = None

    # Set n jobs
    args['n_jobs'] = int(args['cores'] * args['scale'])

    # Set times based on partition
    if args['partition'] == 'short':
        args['time'] = '3:00:00'
        args['wait_time'] = 1800
    else:
        args['time'] = '30:00:00'
        args['wait_time'] = 1800

    # Set is low mem flag
    if args['memory'] / args['cores'] <= 2:
        args['low_mem'] = True
    else:
        args['low_mem'] = False

    # Set name also
    args['name'] = get_name(args['parcel'], args['model'], args['target'])

    print('args:', args, flush=True)
    return args
