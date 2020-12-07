import numpy as np
import nibabel as nib
import os
import nilearn.datasets

from helpers import (conv_to_array_32k_space, conv_matlab,
                     merge, vol_labels_to_surf,
                     prob_vol_labels_to_surf, load_medial_wall,
                     fsaverage_label_to_fs_lr)

def proc_balsa(save_dr):
    
    gordon = conv_to_array_32k_space('../raw/gordon_balsa/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii')
    save_loc = os.path.join(save_dr, 'gordon.npy')
    np.save(save_loc, gordon)
    
    brodmann = conv_to_array_32k_space('../raw/gordon_balsa/Human.Brodmann09.32k_fs_LR.dlabel.nii')
    save_loc = os.path.join(save_dr, 'brodmann.npy')
    np.save(save_loc, brodmann)
    
    vdg11b = conv_to_array_32k_space('../raw/gordon_balsa/Human.Composite_VDG11.32k_fs_LR.dlabel.nii')
    save_loc = os.path.join(save_dr, 'vdg11b.npy')
    np.save(save_loc, vdg11b)

def proc_hcp(save_dr):
    
    lh = conv_to_array_32k_space('../raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    rh = conv_to_array_32k_space('../raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    hcp_mmp = merge(lh, rh)
    
    save_loc = os.path.join(save_dr, 'hcp_mmp.npy')
    np.save(save_loc, hcp_mmp)

def proc_abox(save_dr):

    lh_map = nib.load('../raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]
    rh_map = nib.load('../raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]

    a_dr = '../raw/arslan_box/'
    parcs = os.listdir(a_dr)
    for parc in parcs:
        base = os.path.join(a_dr, parc, parc)
        lh_loc, rh_loc = base + '_L.mat', base + '_R.mat'
        data = conv_matlab(lh_loc, rh_loc, lh_map, rh_map)
        save_loc = os.path.join(save_dr, parc.lower() + '_abox')
        np.save(save_loc, data)

def proc_dlab(save_dr):
    
    dr = '../raw/diedrichsen_lab/'
    parcs = os.listdir(dr)
    parcs = set([p.replace('.R.', '.L.') for p in parcs])

    for p in parcs:
        loc = os.path.join(dr, p)
        lh = conv_to_array_32k_space(loc)
        rh = conv_to_array_32k_space(loc.replace('.L.', '.R.'))
        data = merge(lh, rh)
        save_loc = os.path.join(save_dr, p.split('.')[0].lower() + '_dlab.npy')
        np.save(save_loc, data)

def proc_schaefer(save_dr):
    
    for size in range(100, 1001, 100):
        loc = '../raw/schaefer_cifti/Schaefer2018_' + str(size) + 'Parcels_7Networks_order.dscalar.nii'
        data = conv_to_array_32k_space(loc)
        save_loc = os.path.join(save_dr, 'schaefer_' + str(size))
        np.save(save_loc, data)

def proc_yeo(save_dr):

    y1 = nib.load('../raw/yeo/Yeo2011_7Networks_N1000.dscalar.nii').get_fdata()
    y1 = y1.squeeze()
    save_loc = os.path.join(save_dr, 'yeo_7networks.npy')
    np.save(save_loc, y1)

    y2 = nib.load('../raw/yeo/Yeo2011_17Networks_N1000.dscalar.nii').get_fdata()
    y2 = y2.squeeze()
    save_loc = os.path.join(save_dr, 'yeo_17networks.npy')
    np.save(save_loc, y2)

def proc_maps_and_parcs(save_dr):
    
    for stub in ['economo', 'mesulam', 'oasis.chubs', 'sjh']:

        surf = fsaverage_label_to_fs_lr(lh_loc='../raw/maps_and_parcs/lh.' + stub + '.annot',
                                        rh_loc='../raw/maps_and_parcs/rh.' + stub + '.annot')
        save_loc = os.path.join(save_dr, stub + '.npy')
        np.save(save_loc, surf)

def proc_multi_atlas(save_dr):

    for stub in ['aicha', 'nspn500']:

        surf = fsaverage_label_to_fs_lr(lh_loc='../raw/multi_atlas/lh.' + stub + '.annot',
                                        rh_loc='../raw/multi_atlas/rh.' + stub + '.annot')
        save_loc = os.path.join(save_dr, stub + '.npy')
        np.save(save_loc, surf)

def proc_harvard_oxford(save_dr, mw_mask):

    # Process the single version
    harvard_single_maps = ['cort-maxprob-thr0-1mm', 'cort-maxprob-thr25-1mm',
                           'cort-maxprob-thr50-1mm']

    for single_map in harvard_single_maps:
        loc = nilearn.datasets.fetch_atlas_harvard_oxford(single_map)['maps']
        surf = vol_labels_to_surf(nib.load(loc))

        # Apply medial wall mask
        surf[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-harvard-oxford-' + single_map)
        np.save(save_loc, surf)

    # Process the prob. version
    harvard_prob_map = nilearn.datasets.fetch_atlas_harvard_oxford('cort-prob-1mm')
    vol = nib.load(harvard_prob_map['maps'])
    surfs = prob_vol_labels_to_surf(vol)

    # Apply medial wall mask
    surfs[mw_mask] = 0

    save_loc = os.path.join(save_dr, 'vol-resamp-harvard-oxford-cort-prob-1mm_prob')
    np.save(save_loc, surfs)

def proc_smith(save_dr, mw_mask):

    smith = nilearn.datasets.fetch_atlas_smith_2009()
    for name in ['rsn70', 'bm70']:
        surfs = prob_vol_labels_to_surf(nib.load(smith[name]))
        surfs[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-smith-' + name + '_prob')
        np.save(save_loc, surfs)

def proc_craddock(save_dr, mw_mask):

    c = nilearn.datasets.fetch_atlas_craddock_2012()
    for name in ['tcorr_mean', 'scorr_2level', 'tcorr_2level', 'scorr_mean']:
        surfs = prob_vol_labels_to_surf(nib.load(c[name]))
        surfs[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-craddock-' + name + '_prob')
        np.save(save_loc, surfs)

def proc_aal(save_dr, mw_mask):

    aal = nilearn.datasets.fetch_atlas_aal()
    surf = vol_labels_to_surf(nib.load(aal['maps']))
    surf[mw_mask] = 0

    save_loc = os.path.join(save_dr, 'vol-resamp-aal')
    np.save(save_loc, surf)

def proc_basc(save_dr, mw_mask):

    basc = nilearn.datasets.fetch_atlas_basc_multiscale_2015()
    for scale in ['scale007', 'scale012', 'scale020',
                  'scale036', 'scale064', 'scale122',
                  'scale197', 'scale325', 'scale444']:

        surf = vol_labels_to_surf(nib.load(basc[scale]))
        surf[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-basc-' + scale)
        np.save(save_loc, surf)

def proc_allen(save_dr, mw_mask):

    allen = nilearn.datasets.fetch_atlas_allen_2011()
    surfs = prob_vol_labels_to_surf(nib.load(allen['maps']))
    surfs[mw_mask] = 0

    save_loc = os.path.join(save_dr, 'vol-resamp-allen_prob')
    np.save(save_loc, surfs)

def proc_brainnetome(save_dr, mw_mask):

    vol = nib.load('../raw/brainnetome/BN_Atlas_246_1mm.nii.gz')
    surf = vol_labels_to_surf(vol)
    surf[mw_mask] = 0

    save_loc = os.path.join(save_dr, 'vol-resamp-brainnetome')
    np.save(save_loc, surf)

def proc_shen(save_dr, mw_mask):
    
    for name in ['268', '368']:
        vol = nib.load('../raw/shen/shen_1mm_' + name + '_parcellation.nii.gz')
        surf = vol_labels_to_surf(vol)
        surf[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-shen-' + name)
        np.save(save_loc, surf)

def proc_mist(save_dr, mw_mask):

    for name in ['7','12', '20', '36', '64', '122', '197', '325', '444']:
        surf = vol_labels_to_surf('../raw/mist/MIST_' + name + '.nii.gz')
        surf[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-mist-' + name)
        np.save(save_loc, surf)

def proc_difumo(save_dr, mw_mask):

    for name in ['64', '128', '256', '512', '1024']:
        surfs = prob_vol_labels_to_surf('../raw/difumo/' + name + '.nii.gz')
        surfs[mw_mask] = 0

        save_loc = os.path.join(save_dr, 'vol-resamp-difumo-' + name + '_prob')
        np.save(save_loc, surfs)

def proc_msdl(save_dr, mw_mask):

    msdl = nilearn.datasets.fetch_atlas_msdl()
    surfs = prob_vol_labels_to_surf(msdl['maps'])
    surfs[mw_mask] = 0

    save_loc = os.path.join(save_dr, 'vol-resamp-msdl_prob')
    np.save(save_loc, surfs)

def proc_neuro_parc(save_dr, mw_mask):

    dr = '../raw/neuro_parc/'
    files = os.listdir(dr)
    for file in files:
        surf = vol_labels_to_surf(os.path.join(dr, file))
        surf[mw_mask] = 0
        name = file.split('_')[0]
        save_loc = os.path.join(save_dr, 'vol-resamp-' + name)
        np.save(save_loc, surf)


def main():

    save_dr = '../parcels/'
    os.makedirs(save_dr, exist_ok=True)

    # Proc already surf, already FS_lr_32k space
    proc_balsa(save_dr)
    proc_hcp(save_dr)
    proc_abox(save_dr)
    proc_dlab(save_dr)
    proc_schaefer(save_dr)
    proc_yeo(save_dr)

    # Resample from fs-average to FS_lr_32k
    proc_maps_and_parcs(save_dr)
    proc_multi_atlas(save_dr)

    # Proc sampling dif MNI volumes to surf
    # Load mw_mask - as sampling is noisy, apply this mask
    # to all re-sampled from volume
    mw_mask =\
        load_medial_wall(annot_loc='../raw/fs_LR_32k_label/medialwall.annot')

    proc_harvard_oxford(save_dr, mw_mask)
    proc_smith(save_dr, mw_mask)
    proc_craddock(save_dr, mw_mask)
    proc_aal(save_dr, mw_mask)
    proc_basc(save_dr, mw_mask)
    proc_allen(save_dr, mw_mask)
    proc_brainnetome(save_dr, mw_mask)
    proc_shen(save_dr, mw_mask)
    proc_mist(save_dr, mw_mask)
    proc_difumo(save_dr, mw_mask)
    proc_msdl(save_dr, mw_mask)
    proc_neuro_parc(save_dr, mw_mask)

if __name__ == "__main__":
    main()