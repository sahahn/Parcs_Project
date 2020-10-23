import pandas as pd
import os
import numpy as np

def load_from_rds(names):
    
    data = pd.read_csv('raw/nda_rds_201.csv', usecols=['src_subject_id', 'eventname'] + names, na_values=['777', 999, '999', 777])
    data = data.loc[data[data['eventname'] == 'baseline_year_1_arm_1'].index]
    data = data.set_index('src_subject_id')
    data = data.drop('eventname', axis=1)
    
    return data

def main():

    # Load the variables which can be loaded directly
    data = load_from_rds([
    'sex_at_birth',
    'interview_age',
    'neurocog_pc1.bl',
    'neurocog_pc2.bl',
    'neurocog_pc3.bl',
    'anthro_height_calc',
    'anthro_weight_calc',
    'anthro_waist_cm',
    'devhx_2_birth_wt_lbs_p',
    'devhx_5_twin_p',
    'devhx_12a_born_premature_p',
    'devhx_6_pregnancy_planned_p',
    'devhx_20_motor_dev_p',
    'demo_prnt_age_p',
    'cbcl_scr_syn_rulebreak_r',
    'lmt_scr_perc_correct',
    'macvs_ss_r_p',
    'nihtbx_cardsort_uncorrected', 
    'nihtbx_list_uncorrected',
    'nihtbx_pattern_uncorrected',
    'nihtbx_picvocab_uncorrected',
    'nihtbx_reading_uncorrected',
    'pea_wiscv_trs',
    'accult_phenx_q2_p',
    'ksads_back_c_det_susp_p',
    'ksads_back_c_mh_sa_p',
    'married.bl',
    'neighb_phenx_ss_mean_p',
    'rel_family_id'
    ])

    # Fix weird categories
    data['ksads_back_c_mh_sa_p'] =\
        data['ksads_back_c_mh_sa_p'].replace({'Yes': 1, 'Not sure': np.nan}).astype('float')

    # Add some composites for sports activity
    sp = 'sports_activity_activities_p___'

    # Add composite sum of team sport activites
    team_sport = load_from_rds([sp + str(i) for i in [1,2,4,5,7,11,12,15,21]])
    data['sports_activity_activities_p_team_sport'] = (team_sport != 'not endorsed').sum(axis=1)

    # Add compositive of performance, i.e., Ballet, Music, Drawing ... 
    performance = load_from_rds([sp + str(i) for i in [0,23,24,25]])
    data['sports_activity_activities_p_performance'] = (performance != 'not endorsed').sum(axis=1)

    # Load base variables to binarize
    to_binary = load_from_rds(['devhx_15_days_incubator_p',
                               'asr_scr_thought_r',
                               'cbcl_scr_syn_aggressive_r',
                               'devhx_18_mnths_breast_fed_p',
                               'prodrom_psych_ss_severity_score',
                               'sleep_ss_total_p'])

    # Add the different composites to binarize

    # Add distress at birth
    rep_dic = {"No": 0, "Don't know": 0, "Yes": 1}

    devhx_vars = ['devhx_14a_blue_birth_p', 'devhx_14b_slow_heart_beat_p', 'devhx_14c_did_not_breathe_p',
                'devhx_14d_convulsions_p', 'devhx_14e_jaundice_p', 'devhx_14f_oxygen_p',
                'devhx_14g_blood_transfuse_p', 'devhx_14h_rh_incompatible_p']

    d_at_birth = load_from_rds(devhx_vars)
    d_at_birth.replace(rep_dic, inplace=True)
    to_binary['devhx_distress_at_birth'] = d_at_birth.sum(axis=1)

    # Add mother problems
    devhx_vars = ['devhx_10a_severe_nausea_p', 'devhx_10b_heavy_bleeding_p',
                'devhx_10c_eclampsia_p', 'devhx_10e_persist_proteinuria_p', 'devhx_10d_gall_bladder_p',
                'devhx_10f_rubella_p', 'devhx_10g_severe_anemia_p', 'devhx_10h_urinary_infections_p',
                'devhx_10i_diabetes_p', 'devhx_10j_high_blood_press_p', 'devhx_10k_problems_placenta_p',
                'devhx_10l_accident_injury_p', 'devhx_10m_other_p']

    m_probs = load_from_rds(devhx_vars)
    m_probs.replace(rep_dic, inplace=True)
    to_binary['devhx_mother_probs'] = m_probs.sum(axis=1)

    # Add composite alc
    avg_alc = load_from_rds(['devhx_ss_8_alcohol_avg_p', 'devhx_ss_9_alcohol_avg_p'])
    to_binary['devhx_ss_alcohol_avg_p'] = avg_alc.sum(axis=1)

    # Add composite marijuana
    m_sum = load_from_rds(['devhx_ss_8_marijuana_amt_p', 'devhx_ss_9_marijuana_amt_p'])
    to_binary['devhx_ss_marijuana_amt_p'] = m_sum.sum(axis=1)

    # Add screentime composites
    st = load_from_rds(['screentime_1_hours_p', 'screentime_1_minutes_p',
                        'screentime_2_hours_p', 'screentime_2_minutes_p'])
    to_binary['screentime_week_p'] = st['screentime_1_hours_p'] + (st['screentime_1_minutes_p']/60)
    to_binary['screentime_weekend_p'] = st['screentime_2_hours_p'] + (st['screentime_2_minutes_p']/60)

    # Add ADHD composite
    adhd = load_from_rds(['ksads_14_853_p', 'ksads_14_854_p', 'ksads_14_855_p', 'ksads_14_856_p'])
    to_binary['ksads_adhd_composite'] = adhd.sum(axis=1)

    # Add bipolar composite
    bipolar = load_from_rds(['ksads_2_830_p', 'ksads_2_830_t', 'ksads_2_831_p',
                            'ksads_2_831_t', 'ksads_2_832_p',
                            'ksads_2_832_t', 'ksads_2_833_p',
                            'ksads_2_833_t', 'ksads_2_834_p',
                            'ksads_2_834_t', 'ksads_2_835_p',
                            'ksads_2_835_t', 'ksads_2_836_p',
                            'ksads_2_836_t', 'ksads_2_837_p',
                            'ksads_2_837_t', 'ksads_2_838_p',
                            'ksads_2_838_t', 'ksads_2_839_p',
                            'ksads_2_839_t'])
    to_binary['ksads_bipolar_composite'] = bipolar.sum(axis=1)

    # Add OCD
    ocd = load_from_rds(['ksads_11_917_p', 'ksads_11_918_p', 'ksads_11_919_p', 'ksads_11_920_p'])
    to_binary['ksads_OCD_composite'] = ocd.sum(axis=1)


    # Using the following thresholds to
    # convert to_binary, to binarized versions of each column
    o_dict = {
    'asr_scr_thought_r': 2,
    'cbcl_scr_syn_aggressive_r': 4,
    'prodrom_psych_ss_severity_score': 10,
    'sleep_ss_total_p': 35,
    'devhx_15_days_incubator_p': 0.5,
    'devhx_18_mnths_breast_fed_p': 10,
    'devhx_distress_at_birth': 0.5,
    'devhx_mother_probs': 0.5,
    'devhx_ss_alcohol_avg_p': 0.5,
    'devhx_ss_marijuana_amt_p': 0.5,
    'screentime_week_p': 4,
    'screentime_weekend_p': 5,
    'ksads_adhd_composite': .5,
    'ksads_bipolar_composite': .5,
    'ksads_OCD_composite': .5,
    }

    # Convert, deleting column after done
    cols = list(to_binary)
    for col in cols:
        to_binary[col + '_binary'] = (to_binary[col] > o_dict[col])
        to_binary = to_binary.drop(col, axis=1)

    # Merge to_binary with data
    data = data.merge(to_binary, on='src_subject_id', how='outer')

    # Save as csv for future use
    os.makedirs('data/', exist_ok=True)
    data.to_csv('data/targets.csv')

if __name__ == "__main__":
    main()