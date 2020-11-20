import os
import numpy as np
import pandas as pd
import time
import random
import sys
import shutil

#models = ['elastic', 'lgbm', 'svm']
models = ['elastic', 'lgbm', 'svm']

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
        
        if model in models:
            result = np.load(os.path.join(results_dr, file))
        
            if len(result) > 1:
                try:
                    parcs_counts[parc] += 1
                except KeyError:
                    parcs_counts[parc] = 1

    all_parc_keys = list(parcs_counts)
    random.shuffle(all_parc_keys)
    
    for end in ['' , '1', '2', '3', '4', '5']:
        dr = os.path.join(scratch_dr, 'cache' + end)
        if os.path.exists(dr):
            for parc in all_parc_keys:
                if parcs_counts[parc] == total:
                    cache_dr = os.path.join(dr, parc)
                    if os.path.exists(cache_dr):
                        print('DELETE:', cache_dr, flush=True)
                        shutil.rmtree(cache_dr, ignore_errors=True)

def get_done(results_dr):

    # Check which jobs are done
    results = os.listdir(results_dr)
    done = set()

    for result in results:
        name = result.replace('.npy', '')
        r = np.load(os.path.join(results_dr, result))

        # If done add to done
        if len(r) > 1:
            done.add(name)

        # If started less than 30hr ago, treat as done
        elif time.time() - r < 108000:
            done.add(name)

    return done

def get_name(parcel, model, target):

    name = parcel + '---' + model + '---' + target
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

def get_choice(dr):

    # Parcels
    parcel_dr = os.path.join(dr, 'parcels')
    parcels = [p.replace('.npy', '') for p in os.listdir(parcel_dr)]

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
        for model in models:
            for target in targets:
                
                name = get_name(parcel, model, target)
                
                # Only add if not in done
                if name not in done:
                    all_choices.append(name)

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
        save_loc = os.path.join(results_dr, name + '.npy')

        print('Return pmt', parcel, model, target, flush=True)

        # Return this choice
        return parcel, model, target, save_loc

    # If done, return None
    return None, None, None

def unpack_args():

    base = list(sys.argv)[1:]
    
    args = {'parcel': base[0],
            'model': base[1],
            'target': base[2],
            'save_loc': base[3],
            'memory': int(float(base[4])),
            'partition': base[5],
            'cores': int(float(base[6])),
            'scale': int(float(base[7]))}

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
