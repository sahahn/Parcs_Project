import glob
import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed

from helpers import extract_rois, conv_to_array_32k_space

def extract_fs_rois(parc='aparc.a2009s'):

    print('Extract Freesurfer ROIs parc = ', parc)
    glob_path = '../raw/derivatives/freesurfer-5.3.0-HCP/*/ses-baselineYear1Arm1/stats/*.' + parc + '.stats'

    # Extract the destr ROIs straight from freesurfer
    dicts = {}
    for file in glob.glob(glob_path):
        as_dict = extract_rois(file)
        subj = file.split('/')[-4].split('-')[1]

        try:
            dicts[subj].update(as_dict)
        except KeyError:
            dicts[subj] = as_dict
        
    data = pd.DataFrame.from_dict(dicts, orient='index')
    data.index.name = 'src_subject_id'

    save_loc = '../data/' + parc + '_rois.csv'
    print('save_loc:', save_loc)
    
    data.to_csv(save_loc)


def resave_data():

    # Re-save all data as numpy arrays w/ dif file structure
    save_dr = '../data/abcd_structural/'
    os.makedirs(save_dr, exist_ok=True)

    stubs = {'_curv.dscalar.nii' : 'curv',
             '_myelinmap.dscalar.nii': 'myelin',
             '_sulc.dscalar.nii' : 'sulc',
             '_thickness.dscalar.nii': 'thick'}

    base = '../raw/derivatives/abcd-hcp-pipeline/'
    base += 'sub-*/ses-baselineYear1Arm1/anat/'
    base += 'sub-*_ses-baselineYear1Arm1_space-fsLR32k'

    def resave(file):
        # Determine save loc
        subj = file.split('/')[-4].replace('sub-NDAR', '')
        save_loc = os.path.join(dr, subj + '.npy')
        
        # Load the data in full space
        data = conv_to_array_32k_space(file)
        
        # Cast to float32 - this was the original resolution
        data = data.astype('float32')

        # Save as np array
        np.save(save_loc, data)

    for stub in stubs:
        
        # Make intermediate dr
        dr = os.path.join(save_dr, stubs[stub])
        os.makedirs(dr, exist_ok=True)
        
        # Get all files
        files = glob.glob(base + stub)
        Parallel(n_jobs=16)(delayed(resave)(file) for file in files)

def main():

    # Destr
    extract_fs_rois('aparc.a2009s')

    # Freesurfer
    extract_fs_rois('aparc')
    
    # Resave main data as numpy arrays
    resave_data()
    

if __name__ == "__main__":
    main()
    