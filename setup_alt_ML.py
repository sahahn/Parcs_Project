import pandas as pd
import numpy as np
import os
from setup_ML import load_base
from BPt import *

def main():

    # Setup alternate ML object with logs
    ML = BPt_ML(log_dr='setup_alt_ML_Logs',
                existing_log='overwrite',
                verbose=True,
                random_state=5,
                notebook=False,
                mp_context='loky',
                n_jobs=32)

    # Load targets and Strat
    ML = load_base(ML, show_dist=False)

    # Limit to just train subjects
    ML.Load_Inclusions(loc='setup_ML_Logs/My_Exp/train_subjects.txt')

    # Load Alternate Freesurfer Extracted ROIs
    data = pd.read_csv('data/aparc.a2009s_rois.csv')
    data['src_subject_id'] = [s.replace('NDAR', 'NDAR_') for s in data['src_subject_id']]

    ML.Load_Data(df=data,
                 inclusion_keys=['_thickavg', '_surfarea', '_meancurv'],
                 drop_na=False)

    # Need to line up with other
    ML.Prepare_All_Data(merge='outer')

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
