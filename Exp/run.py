import os
import sys
from helpers import get_choice, clean_cache
import random
import numpy as np

def is_binary(target):

    binary = ['devhx_distress_at_birth_binary', 'ksads_back_c_det_susp_p',
              'screentime_weekend_p_binary',
              'prodrom_psych_ss_severity_score_binary', 'married.bl',
              'asr_scr_thought_r_binary', 'accult_phenx_q2_p', 'devhx_5_twin_p',
              'ksads_adhd_composite_binary',
              'devhx_18_mnths_breast_fed_p_binary', 'sex_at_birth',
              'devhx_ss_marijuana_amt_p_binary', 'devhx_ss_alcohol_avg_p_binary',
              'ksads_bipolar_composite_binary', 'devhx_6_pregnancy_planned_p',
              'devhx_mother_probs_binary', 'screentime_week_p_binary',
              'devhx_12a_born_premature_p', 'devhx_15_days_incubator_p_binary',
              'ksads_back_c_mh_sa_p', 'sleep_ss_total_p_binary',
              'cbcl_scr_syn_aggressive_r_binary', 'ksads_OCD_composite_binary']

    return target in binary

# Main directory
dr = '/users/s/a/sahahn/Parcs_Project/'

try:
    n_submit = int(float(sys.argv[1]))
except IndexError:
    n_submit = 1

submitted = 0
trys = 0

max_trys = 10 * n_submit
max_trys = min([max_trys, 30])

while submitted < n_submit and trys < max_trys:

    trys += 1

    # Get parcel, model, target to run
    parcel, model, target, split, save_loc = get_choice(dr)
    if parcel is None:
        break
    
    # Get parcel size
    # If stacked... determine differently - NOTE may want to factor in the nested-ness...
    if parcel.startswith('stacked_random'):
        base_parcel_size = int(parcel.split('_')[2])
        n_parcels = int(parcel.split('_')[3])
        parcel_size = (base_parcel_size * n_parcels) + 100

    # Otherwise load
    else:
        p = np.load('../parcels/' + parcel + '.npy')
        if len(p.shape) == 2:
            parcel_size = p.shape[1]
        else:
            parcel_size = len(np.unique(p))

    # NOTE - may want to change caclulations based on if split

    # Set if needs high memory
    hi_mem = False

    if parcel_size >= 800:
        hi_mem = True

    if model in set(['lgbm', 'svm']) and parcel_size >= 500:
        hi_mem = True

    # Set if needs short queue
    short = True

    if parcel_size >= 550:
        short = False

    if model == 'svm' and parcel_size >= 350 and is_binary(target):
        short = False

    if model == 'lgbm' and parcel_size < 1000 and not is_binary(target):
        short = True

    if model == 'elastic' and parcel_size <= 1000:
        short = True

    if model == 'elastic' and parcel_size <= 1500 and not is_binary(target):
        short = True

    # Set extra
    extra = False

    # If between 200 and 550 and svm, set extra
    if parcel_size >= 200 and parcel_size < 550 and model == 'svm':
        extra = True

    if parcel_size >= 500 and model == 'lgbm' and is_binary(target):
        extra = True

    # ONLY RUNNING WITH SHORT QUEUE
    if not short:
        continue

    # Job name gets filled in
    job_name = ''

    # Base 4 cores for now
    cores = 4

    # Set job memory
    if hi_mem:
        mem_per_cpu = '8G'
        mem = int(cores * 5)
        job_name += 'high_'
    else:
        mem_per_cpu = '4G'
        mem = int(cores * 2)
        job_name += 'low_'

    # Always short - for now
    partition = 'short'
    time = '3:00:00'
    job_name += 'short'

    # Proc if in extra, set higher scale
    if extra:
        scale = 12
        job_name += '_extra'
    else:
        scale = 6

    # Sbatch commands
    cmd = 'sbatch --mem=' + mem_per_cpu + ' '
    cmd += '--job-name=' + job_name + ' '
    cmd += '--partition=' + partition + ' ' 
    cmd += '--time=' + time + ' '

    # Job commands
    cmd += 'submit_job.sh '
    cmd += parcel + ' '
    cmd += model + ' '
    cmd += target + ' '
    cmd += str(split) + ' '
    cmd += save_loc + ' '
    cmd += str(mem) + ' '
    cmd += partition + ' '
    cmd += str(cores) + ' '
    cmd += str(scale) + ' '

    # Submit job
    os.system(cmd)
    submitted += 1

    print('Submitted: ', cmd, flush=True)
    

if trys >= 30:
    print('No more short jobs found!', flush=True)

# Once done submitting
clean_cache(dr=dr, scratch_dr='/users/s/a/sahahn/scratch/')
