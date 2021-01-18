# raw

The raw folder contains all of the different data sources referenced for this project. Donwloads were made in Novemember 2020.

The following sections describe the contents of each folder (note: that some cannot be uploaded due to data use agreements)

--------------
### derivatives/

The derivatives folder was downloaded from the DCAN ABCD data collection https://collection3165.readthedocs.io/en/stable/derivatives/
Using the https://github.com/DCAN-Labs/nda-abcd-s3-downloader 

The file structure looks like this:

- raw/derivatives/
- raw/derivatives/abcd-hcp-pipeline/...
- raw/derivatives/freesurfer-5.3.0-HCP/...


The following files were specified using the download tool:

- derivatives.anat.space-fsLR32k_curv
- derivatives.anat.space-fsLR32k_myelinmap
- derivatives.anat.space-fsLR32k_sulc
- derivatives.anat.space-fsLR32k_thickness
- derivatives.anat.stats

Due to data use agreements, this folder and the data within cannot be shared here.

-----------------

### nda_rds_201.csv

This folder represents the DEAP rds version 2.0.1 as converted to a csv.
Due to data use agreements, this folder and the data within cannot be shared here.
In order to create this file, the rds was simply loaded as a dataframe in R and then saved as a csv. 

----------------

### shaefer_cifti/

The shaefer_cifti folder was downloaded from https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/HCP/fslr32k/cifti 

The folder was renamed shaefer_cifti, and only 10 files kept, corresponding to the 100 to 1000 Parcels versions, e.g.,

- raw/schaefer_cifti/Schaefer2018_100Parcels_7Networks_order.dscalar.nii
- raw/schaefer_cifti/Schaefer2018_200Parcels_7Networks_order.dscalar.nii
- ...
- raw/schaefer_cifti/Schaefer2018_1000Parcels_7Networks_order.dscalar.nii

------------

### gordon_balsa/

The following files were downloaded from https://balsa.wustl.edu/WK71 

- raw/gordon_balsa/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii
- raw/gordon_balsa/Human.Brodmann09.32k_fs_LR.dlabel.nii
- raw/gordon_balsa/Human.Composite_VDG11.32k_fs_LR.dlabel.nii

-----------------

### hcp_mmp_balsa

The following files were downloed from https://balsa.wustl.edu/WN56

- raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii
- raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii

-------------------

### arslan_box

The Group folder from https://imperialcollegelondon.app.box.com/s/g5q0kyvpqdha5jgofhmiov9ws1ao0hi0/ was downloaded, and renamed arslan_box.

Example file paths:
- raw/arslan_box/AAL/AAL_L.mat
- raw/arslan_box/AAL/AAL_R.mat

-------------------

### diedrichsen_lab

The following folder was downloaded from https://github.com/DiedrichsenLab/fs_LR_32

Example files paths:
- raw/diedrichsen_lab/Desikan.32k.L.label.gii
- raw/diedrichsen_lab/Desikan.32k.R.label.gii


-------------------

### mist

The following folder was downloaded from https://figshare.com/articles/MIST_A_multi-resolution_parcellation_of_functional_networks/5633638
The parcellations are then re-sampled from this original volumetric space.

-------------------

### difumo

The following folder was downloaded from https://parietal-inria.github.io/DiFuMo/
Note: this folder was rather large so it was not uploaded to this git, but the following files were downloaded (and renamed!)
They represent the highest resolution avaliable for each of the scales of parcellations.
The parcellations are then re-sampled from this original volumetric space.

-raw/difumo/64.nii.gz
-raw/difumo/128.nii.gz
-raw/difumo/256.nii.gz
-raw/difumo/512.nii.gz
-raw/difumo/1024.nii.gz

-------------------

### brainnetome

The 1mm volumetric brainnetome atlas was downloaded from http://www.brainnetome.org/resource/


### shen

Two shen volumetric parcellations are downloaded from https://www.nitrc.org/frs/download.php/11629/shen_368.zip and https://github.com/canlab/Neuroimaging_Pattern_Masks/tree/master/Atlases_and_parcellations/2013_Shen_Constable_NIMG_268_parcellation

The two downloaded files are both volumetric (and later re-sampled), one (newer) has 268 parcels and the (older) 268.

-------------------

### yeo

The two yeo 7 networks and 17 networks parcellations were downloaded from:
https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Yeo2011_fcMRI_clustering/1000subjects_reference/Yeo_JNeurophysiol11_SplitLabels/fs_LR32k


-------------------


### maps_and_parcs

Five different parcellations, economo, economo7, mesulam, oasis.chubs and shj were downloaded from
https://github.com/ucam-department-of-psychiatry/maps_and_parcs/tree/master/Parcellations/FSAverage
These parcellations are downloaded in fsaverage space seperate for left and right hemispheres.

-------------------

### multi_atlas

Two parcellations, aicha and spn500, were downloaded from https://github.com/faskowit/multiAtlasTT/tree/master/atlas_data
with each parcellation within its own folders, but extracted here.
These parcellations were downloaded in fsaverage space seperate for left and right hemispheres.

-------------------

### neuro_parc

Eight volumetric parcellations were downloaded from https://github.com/neurodata/neuroparc/tree/master/atlases/label/Human

These have not been added to the git due to space, but the following files were downloaded:

- raw/neuro_parc/CAPRSC_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/CPAC200_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/Hammersmith_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/JHU_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/Juelich_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/MICCAI_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/Princetonvisual-top_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/Slab907_space-MNI152NLin6_res-1x1x1.nii.gz
- raw/neuro_parc/Slab1068_space-MNI152NLin6_res-1x1x1.nii.gz

-------------------

### standard_mesh_atlases

Downloaded from http://brainvis.wustl.edu/workbench/standard_mesh_atlases.zip

These files are used to generate new random parcellations and during resampling from
fsaverage to LR_fs_32k standard space.

----------------------

### fs_LR_32k_label

Downloaded from https://github.com/ThomasYeoLab/CBIG/tree/master/data/templates/surface/fs_LR_32k/label
Includes only the medialwall.annot file. This is a mask with 0's indicating where in the fs_LR_32k space there is medial wall.







