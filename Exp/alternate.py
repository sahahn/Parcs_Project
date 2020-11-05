from BPt import *
from models import get_pipe
import os
import numpy as np

def main():

    ML = Load('/users/s/a/sahahn/Parcs_Project/data/Alt.ML', log_dr=None)
    ML.n_jobs = 8

    # CV
    cv = CV(groups='rel_family_id')

    # Run Comparison
    for target in ML.targets_keys:
        for model in ['elastic']:
            
            # Get pipe, but set loaders to None, and dask_ip to None
            pipeline = get_pipe(model, '', cv=cv, dask_ip=None)
            pipeline.loaders = None
            
            # Get name
            name = 'freesurfer_destr---' + model + '---' + target + '.npy'
            print(name)
            
            # Only run if not run before
            done = os.listdir('results')
            if name not in done:
            
                # Run with 5 repeats
                results = ML.Evaluate(model_pipeline=pipeline,
                                      problem_spec=Problem_Spec(target=target),
                                      splits=5,
                                      n_repeats=5,
                                      cv=cv)
                
                # Save results once done
                np.save('results/' + name, results['summary_scores'])

if __name__ == '__main__':
    main()