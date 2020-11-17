import numpy as np
import nibabel as nib
import os
import nilearn.datasets

from helpers import (conv_to_array_32k_space, conv_matlab,
                     merge, vol_labels_to_surf,
                     prob_vol_labels_to_surf, load_medial_wall)

# Set as global variable
mw_mask =\
    load_medial_wall(annot_loc='raw/fs_LR_32k_label/medialwall.annot')

def proc_balsa():
    
    gordon = conv_to_array_32k_space('raw/gordon_balsa/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii')
    np.save('parcels/gordon.npy', gordon)
    
    brodmann = conv_to_array_32k_space('raw/gordon_balsa/Human.Brodmann09.32k_fs_LR.dlabel.nii')
    np.save('parcels/brodmann.npy', brodmann)
    
    vdg11b = conv_to_array_32k_space('raw/gordon_balsa/Human.Composite_VDG11.32k_fs_LR.dlabel.nii')
    np.save('parcels/vdg11b.npy', vdg11b)

def proc_hcp():
    
    lh = conv_to_array_32k_space('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    rh = conv_to_array_32k_space('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    hcp_mmp = merge(lh, rh)
    np.save('parcels/hcp_mmp.npy', hcp_mmp)

def proc_abox():

    lh_map = nib.load('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]
    rh_map = nib.load('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]

    a_dr = 'raw/arslan_box/'
    parcs = os.listdir(a_dr)
    for parc in parcs:
        base = os.path.join(a_dr, parc, parc)
        lh_loc, rh_loc = base + '_L.mat', base + '_R.mat'
        data = conv_matlab(lh_loc, rh_loc, lh_map, rh_map)
        np.save('parcels/' + parc.lower() + '_abox', data)

def proc_dlab():
    
    dr = 'raw/diedrichsen_lab/'
    parcs = os.listdir(dr)
    parcs = set([p.replace('.R.', '.L.') for p in parcs])

    for p in parcs:
        loc = os.path.join(dr, p)
        lh = conv_to_array_32k_space(loc)
        rh = conv_to_array_32k_space(loc.replace('.L.', '.R.'))
        data = merge(lh, rh)
        np.save('parcels/' + p.split('.')[0].lower() + '_dlab.npy', data)

def proc_schaefer():
    
    for size in range(100, 1001, 100):
        loc = 'raw/schaefer_cifti/Schaefer2018_' + str(size) + 'Parcels_7Networks_order.dscalar.nii'
        data = conv_to_array_32k_space(loc)
        np.save('parcels/schaefer_' + str(size), data)

def proc_harvard_oxford():

    # Process the single version
    harvard_single_maps = ['cort-maxprob-thr0-1mm', 'cort-maxprob-thr25-1mm',
                           'cort-maxprob-thr50-1mm']
    for single_map in harvard_single_maps:
        loc = nilearn.datasets.fetch_atlas_harvard_oxford(single_map)['maps']
        surf = vol_labels_to_surf(nib.load(loc))

        # Apply medial wall mask
        surf[mw_mask] = 0

        np.save('parcels/vol-resamp-harvard-oxford-' + single_map, surf)

    # Process the prob. version
    harvard_prob_map = nilearn.datasets.fetch_atlas_harvard_oxford('cort-prob-1mm')
    vol = nib.load(harvard_prob_map['maps'])
    surfs = prob_vol_labels_to_surf(vol)

    # Apply medial wall mask
    surfs[mw_mask] = 0

    np.save('parcels/vol-resamp-harvard-oxford-cort-prob-1mm_prob', surfs)

def proc_smith():

    smith = nilearn.datasets.fetch_atlas_smith_2009()
    for name in ['rsn70', 'bm70']:
        surfs = prob_vol_labels_to_surf(nib.load(smith[name]))
        surfs[mw_mask] = 0
        np.save('parcels/vol-resamp-smith-' + name + '_prob', surfs)

def proc_craddock():

    c = nilearn.datasets.fetch_atlas_craddock_2012()
    for name in ['tcorr_mean', 'scorr_2level', 'tcorr_2level', 'scorr_mean']:
        surfs = prob_vol_labels_to_surf(nib.load(c[name]))
        surfs[mw_mask] = 0
        np.save('parcels/vol-resamp-craddock-' + name + '_prob', surfs)

def proc_aal():

    aal = nilearn.datasets.fetch_atlas_aal()
    surf = vol_labels_to_surf(nib.load(aal['maps']))
    surf[mw_mask] = 0
    np.save('parcels/vol-resamp-aal', surf)

def proc_basc():

    basc = nilearn.datasets.fetch_atlas_basc_multiscale_2015()
    for scale in ['scale007', 'scale012', 'scale020',
                  'scale036', 'scale064', 'scale122',
                  'scale197', 'scale325', 'scale444']:
        surf = vol_labels_to_surf(nib.load(basc[scale]))
        surf[mw_mask] = 0
        np.save('parcels/vol-resamp-basc-' + scale, surf)

def proc_allen():

    allen = nilearn.datasets.fetch_atlas_allen_2011()
    surfs = prob_vol_labels_to_surf(nib.load(allen['maps']))
    surfs[mw_mask] = 0
    np.save('parcels/vol-resamp-allen_prob', surfs)

def proc_brainnetome():

    vol = nib.load('raw/brainnetome/BN_Atlas_246_1mm.nii.gz')
    surf = vol_labels_to_surf(vol)
    surf[mw_mask] = 0
    np.save('parcels/vol-resamp-brainnetome', surf)

def proc_shen():
    
    for name in ['268', '368']:
        vol = nib.load('raw/shen/shen_1mm_' + name + '_parcellation.nii.gz')
        surf = vol_labels_to_surf(vol)
        surf[mw_mask] = 0
        np.save('parcels/vol-resamp-shen-' + name, surf)

def proc_mist():

    for name in ['7','12', '20', '36', '64', '122', '197', '325', '444']:
        vol = nib.load('raw/mist/MIST_' + name + '.nii.gz')
        surf = vol_labels_to_surf(vol)
        surf[mw_mask] = 0
        np.save('parcels/vol-resamp-mist-' + name, surf)

def proc_difumo():

    for name in ['64', '128', '256', '512', '1024']:
        vol = nib.load('raw/difumo/' + name + '.nii.gz')
        surfs = prob_vol_labels_to_surf(vol)
        surfs[mw_mask] = 0
        np.save('parcels/vol-resamp-difumo-' + name + '_prob', surfs)

def main():

    # Proc already surf
    #proc_balsa()
    #proc_hcp()
    #proc_abox()
    #proc_dlab()
    #proc_schaefer()

    # Proc vol to surf
    #proc_harvard_oxford()
    #proc_smith()
    #proc_craddock()
    #proc_aal()
    #proc_basc()
    #proc_allen()
    #proc_brainnetome()
    #proc_shen()
    #proc_mist()
    proc_difumo()



    

if __name__ == "__main__":
    main()