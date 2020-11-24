# Setup

This folder contains the scripts necessary to setup all of the data, target variables and parcellations needed to run the rest of the project.


### Software Requiriments

--------------------------

The python 3.6+ library Brain Predictability toolbox https://github.com/sahahn/BPt version 1.4 is used extensively. In addition, the python libraries nibabel, nilearn and networkx are requiried.

In addition to the above listed python libraries, both the software FreeSurfer (https://surfer.nmr.mgh.harvard.edu/) and Matlab (https://www.mathworks.com/products/matlab.html) are requiried during a step where originally volumetric parcellations are re-sampled to fsaverage surface space. In addition to these softwares, the scripts needed for this conversion should be downloaded from https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/registration/Wu2017_RegistrationFusion. Once these are installed, make sure to set the relevant locations in config.py.


### Raw Data
--------------------------

This project requires downloading a great deal of raw data from a few different sources. Please view the README at https://github.com/sahahn/Parcs_Project/tree/main/raw for a detailed description of where different things were sourced. Note that the linked raw folder contains a number of these data sources, but due to either data sharing restrictions or size limits, there are missing folders and files which must be filled in by the user in order to use the scripts within Setup.


### Usage
--------------------------

Once config.py has been filled in, there are two scripts which can be used to to run the setup. These are local_setup.sh and slurm_setup.sh. One is designed to run all of the setup steps on a local device and the other is designed to perform the same set of steps, but to be submitted with sbatch slurm_setup.sh on a SLURM cluster. 

Running setup runs the following sub-scripts:

- process_parcs.py : In this script, all of the collected "raw" parcellations within the raw/ folder are converted into ultimately numpy arrays within FS_lr_32k space. This script takes care of any re-sampling or other steps, e.g., combining left and right hemispheres, fsaverage to FS_lr_32k projection, ect... that are needed. All final parcellations are saved within the parcels/ folder (https://github.com/sahahn/Parcs_Project/tree/main/parcels).

- process_random_parcels.py : In this script, a range of random surface parcellations are generated across different sizes and random seeds. The RandomParcels class from BPt extensions is used for this (https://github.com/sahahn/BPt/blob/master/BPt/extensions/RandomParcels.py). 

- process_derivatives.py : This script accomplishes two tasks. First, Desikan and Destr. rois are extracted from the downloaded FreeSurfer stats files for each subject, and then are converted and saved as csv files within data (a directory created at the top structure to hold processed data). Next, all downloaded "raw" surface values are re-saved within data as numpy arrays, e.g., under data/abcd_structural/curv/SUBJ_ID.npy or data/abcd_structural/thick/SUBJ_ID.npy.

- process_targets.py : This script loads and performs some relevant transformations to all of the identified target variables. Raw data is loaded from raw/nda_rds_201.csv. The final csv containing all target variables (and family id) is saved under data/targets.csv. 

- setup_ML.py : This script creates and saved the base BPt ML object. First, target data is loaded and relevant types inferred. Next, all imaging data is loaded and outlier filtering performed on each type of data. Visual distributions for the loaded targets and each type of surface data are included within [setup_ML_Logs/Exp/](https://github.com/sahahn/Parcs_Project/tree/main/Setup/setup_ML_Logs/My_Exp). A version of the data is then saved under data/consolidated where each type of data per subject [curv, thick, myelin, sulc] are stacked per subject (this step is done to save time, and reduce the number of cached files / files to be loaded during later machine learning). Lastly, the prepared ML object is saved under data/Base_consol.ML, where it can be later loaded with as many asynchronus copies as desired and ML expiriments performed.

- setup_alt_ML.py : This script generates an alternate BPt ML object, where instead of loading the raw surface data, the csv's with FreeSurfer derived Desikan and Destr. rois are instead loaded. Valid subjects are restricted to be exactly those that met all of the criteria in creating setup_ML, such that the eventual expiriments run with this seperate data source will match exactly the fold structure from the other expiriments. The output ML object is saved under data/Alt.ML, and simmilar to setup_ML_Logs, setup_alt_ML_Logs contains the detailed log information generated from this loading process (including number of subjects filtered for various reasions, etc...).