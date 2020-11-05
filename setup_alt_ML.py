import pandas as pd
import numpy as np
import os
from setup_ML import load_base
from Exp.models import get_pipe
from BPt import *

def main():

    # Setup alternate ML object with logs
    ML = BPt_ML(log_dr='setup_alt_ML_Logs',
                existing_log='overwrite',
                verbose=True,
                random_state=5,
                notebook=False,
                mp_context='loky',
                n_jobs=16)

    # Load targets and Strat
    ML = load_base(ML, show_dist=False)

    # Load Alternate Freesurfer Extracted ROIs
    data = pd.read_csv('data/rois.csv')
    data['src_subject_id'] = [s.replace('NDAR', 'NDAR_') for s in data['src_subject_id']]

    ML.Load_Data(df=data,
                inclusion_keys=['_thickavg', '_surfarea', '_meancurv'])

    # Set to no test data
    ML.Train_Test_Split(test_size=0)

     # Set some verbosity params
    ML.Set_Default_ML_Verbosity(pipeline_verbose=True,
                                best_params_score=True,
                                fold_name=True,
                                time_per_fold=True,
                                score_per_fold=True,
                                fold_sizes=True,
                                best_params=True,
                                flush=True)

    # Save ML object
    ML.Save('data/Alt.ML', low_memory=True)

if __name__ == '__main__':
    main()