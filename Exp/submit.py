import time
import numpy as np
from BPt import Problem_Spec, CV, Load

from models import get_pipe

def evaluate(args, n_jobs, dask_ip=None):

    print('Running for: ', args['name'], flush=True)

    # Save current time to indicate job is started
    np.save(args['save_loc'], np.array([time.time()]))

    # Load the ML object
    ML = Load('/users/s/a/sahahn/Parcs_Project/data/Base.ML',
            log_dr=None, notebook=False)
    ML.n_jobs = n_jobs

    # Try set flush on
    ML.Set_Default_ML_Verbosity(flush=True)

    # Create the CV group preserve by family id
    cv = CV(groups='rel_family_id')

    # Get the pipeline to evaluate
    pipeline = get_pipe(model_str=args['model'],
                        parcel=args['parcel'],
                        cv=cv,
                        dask_ip=dask_ip)

    # Get the problem spec
    ps = Problem_Spec(target=args['target'])

    # Evaluate this combination with 5 fold CV, two repeats
    results = ML.Evaluate(model_pipeline=pipeline,
                          problem_spec=ps,
                          splits=5,
                          n_repeats=1,
                          CV=cv)

    # Save scores, indicating this job is done
    scores = np.array(results['summary_scores'])
    np.save(args['save_loc'], scores)