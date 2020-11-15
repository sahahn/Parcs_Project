import os
import sys
from helpers import get_choice, clean_cache
import random

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


while submitted < n_submit and trys < 30:

    trys += 1

    # Get parcel, model, target to run
    parcel, model, target, save_loc = get_choice(dr)
    if parcel is None:
        break

    # Base parcs that need high mem
    hi_mem = set(['icosahedron-1002_dlab',
                  'icosahedron-1442_dlab',
                  'schaefer_800',
                  'schaefer_900',
                  'schaefer_1000'])

    # Add random
    for size in [800, 900, 1000]:
        for random_state in range(0, 50):
            hi_mem.add('random_' + str(size) + '_' + str(random_state))

    # If lgbm or svm
    if model in set(['lgbm', 'svm']):
        hi_mem.add('icosahedron-642_dlab')
        hi_mem.add('schaefer_500')
        hi_mem.add('schaefer_600')
        hi_mem.add('schaefer_700')

        for size in [500, 600, 700]:
            for random_state in range(0, 50):
                hi_mem.add('random_' + str(size) + '_' + str(random_state))

    # Base parcs that can run short
    short = set(['schaefer_100',
                 'schaefer_200',
                 'schaefer_300',
                 'schaefer_400',
                 'icosahedron-42_dlab',
                 'vdg11b',
                 'brodmann',
                 'power2011_dlab',
                 'fan_abox',
                 'dextrieux_dlab',
                 'destrieux_abox',
                 'glasser_abox',
                 'gordon',
                 'baldassano_abox',
                 'yeo_abox',
                 'aal_abox',
                 'shen_abox',
                 'desikan_dlab',
                 'desikan_abox',
                 'gordon_abox',
                 ])

    # Add random
    for size in [100, 200, 300, 400]:
        for random_state in range(0, 50):
            short.add('random_' + str(size) + '_' + str(random_state))

    # If elastic or lgbm, extra short
    if model in set(['elastic', 'lgbm']):
        short.add('schaefer_500')
        short.add('schaefer_600')
        short.add('schaefer_700')
        short.add('schaefer_800')
        short.add('schaefer_900')
        short.add('icosahedron-642_dlab')
        short.add('icosahedron-362_dlab')

        for size in [500, 600, 700, 800, 900]:
            for random_state in range(0, 50):
                short.add('random_' + str(size) + '_' + str(random_state))

    if model == 'lgbm' and is_binary(target):
        short.remove('schaefer_500')

        for random_state in range(0, 50):
            short.remove('random_500_' + str(random_state))

    # Add up to 500 if SVM - only regression
    if model == 'svm' and not is_binary(target):
        short.add('schaefer_500')
        for random_state in range(0, 50):
            short.add('random_500_' + str(random_state))

    # Remove 400 if svm and binary
    if model == 'svm' and is_binary(target):
        short.remove('schaefer_400')
        short.remove('glasser_abox')
        for random_state in range(0, 50):
            short.remove('random_400_' + str(random_state))

    # Add 1k to elastic only if not binary
    if model == 'elastic' and not is_binary(target):
        short.add('schaefer_1000')
        for random_state in range(0, 50):
            short.add('random_1000_' + str(random_state))

    # Extra scaled paritions - for all
    extra = set(['icosahedron-1002_dlab',
                 'icosahedron-1442_dlab'])

    # Extra for svm and lgbm
    if model in set(['svm', 'lgbm']):
        extra.add('schaefer_800')
        extra.add('schaefer_900')
        extra.add('schaefer_1000')

        for size in [800, 900, 1000]:
            for random_state in range(0, 50):
                extra.add('random_' + str(size) + '_' + str(random_state))

    if model == 'svm':
        extra.add('glasser_abox')
        extra.add('schaefer_700')
        
        for size in [700]:
            for random_state in range(0, 50):
                extra.add('random_' + str(size) + '_' + str(random_state))

    

    # Job name gets filled in
    job_name = ''

    # Base 4 cores for now
    cores = 4

    # Set job memory
    if parcel in hi_mem:
        mem_per_cpu = '7G'
        mem = int(cores * 5)
        job_name += 'high_'
        
    else:
        mem_per_cpu = '4G'
        mem = int(cores * 2)
        job_name += 'low_'

    # Set parition
    if parcel in short:
        partition = 'short'
        time = '3:00:00'
        job_name += 'short'
    else:

        # For now.. just skip
        continue

        #partition = 'bluemoon'
        #job_name += 'bluemoon'
        #time = '30:00:00'

        # TEMP SUBMIT ALL TO SHORT! - But force to EXTRA
        #partition = 'short'
        #time = '3:00:00'
        #job_name += 'short'
        #extra.add(parcel)

    # Proc if in extra, set higher scale
    if parcel in extra:
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
    cmd += save_loc + ' '
    cmd += str(mem) + ' '
    cmd += partition + ' '
    cmd += str(cores) + ' '
    cmd += str(scale) + ' '

    # Submit job and print
    os.system(cmd)
    print('Submitted: ', cmd, flush=True)

    submitted += 1

if trys >= 30:
    print('No more short jobs found!', flush=True)

# Once done submitting
clean_cache(dr=dr, scratch_dr='/users/s/a/sahahn/scratch/')
