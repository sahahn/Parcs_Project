# raw

The raw folder contains all of the different data sources referenced for this project. Donwloads were made around 10/10/2020. 

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

### standard_mesh_atlases

Downloaded from http://brainvis.wustl.edu/workbench/standard_mesh_atlases.zip only the files:

- raw/standard_mesh_atlases/L.sphere.32k_fs_LR.surf.gii
- raw/standard_mesh_atlases/R.sphere.32k_fs_LR.surf.gii

Are used. They are used to generate new random parcellations.

----------------------

### fs_LR_32k_label

Downloaded from https://github.com/ThomasYeoLab/CBIG/tree/master/data/templates/surface/fs_LR_32k/label
Includes only the medialwall.annot file. This is a mask with 0's indicating where in the fs_LR_32k space there is medial wall.