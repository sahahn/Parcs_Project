import os
import numpy as np
import pandas as pd
import time
import random


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

    name = parcel + '-' + model + '-' + target
    return name

def get_choice(dr):

    # Parcels
    parcel_dr = os.path.join(dr, 'parcels')
    parcels = [p.replace('.npy', '') for p in os.listdir(parcel_dr)]

    # Target names
    data_dr = os.path.join(dr, 'data')
    targets_loc = os.path.join(data_dr, 'targets.csv')
    targets = list(pd.read_csv(targets_loc,
                            index_col='src_subject_id',
                            nrows=0))

    # Models
    models = ['elastic', 'lgbm']

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
        save_loc = os.path.join(results_dr, name + '.npy')
        
        # Return this choice
        return parcel, model, target, save_loc

    # If done, return None
    return None