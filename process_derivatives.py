import glob
import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed

from utils import extract_destr_rois, conv_to_array_32k_space

# Extract the destr ROIs straight from freesurfer
dicts = {}
for file in glob.glob('raw/derivatives/freesurfer-5.3.0-HCP/*/ses-baselineYear1Arm1/stats/*.aparc.a2009s.stats'):
    as_dict = extract_destr_rois(file)
    subj = file.split('/')[3].split('-')[1]

    try:
        dicts[subj].update(as_dict)
    except KeyError:
        dicts[subj] = as_dict
    
data = pd.DataFrame.from_dict(dicts, orient='index')
data.index.name = 'src_subject_id'
data.to_csv('data/rois.csv')

# Re-save all data as numpy arrays w/ dif file structure
save_dr = 'data/abcd_structural/'
os.makedirs(save_dr, exist_ok=True)

stubs = {'_curv.dscalar.nii' : 'curv',
         '_desc-smoothed_myelinmap.dscalar.nii': 'smooth_myelin',
         '_myelinmap.dscalar.nii': 'myelin',
         '_sulc.dscalar.nii' : 'sulc',
         '_thickness.dscalar.nii': 'thick'}

base = 'raw/derivatives/abcd-hcp-pipeline/'
base += 'sub-*/ses-baselineYear1Arm1/anat/'
base += 'sub-*_ses-baselineYear1Arm1_space-fsLR32k'

def resave(file):
    # Determine save loc
    subj = file.split('/')[3].replace('sub-NDAR', '')
    save_loc = os.path.join(dr, subj + '.npy')
    
    # Load the data in full space
    data = conv_to_array_32k_space(file)
    
    # Re-save the data as a numpy array
    np.save(save_loc, data)


for stub in stubs:
    
    # Make intermediate dr
    dr = os.path.join(save_dr, stubs[stub])
    os.makedirs(dr, exist_ok=True)
    
    # Get all files
    files = glob.glob(base + stub)
    Parallel(n_jobs=16)(delayed(resave)(file) for file in files)

        
    