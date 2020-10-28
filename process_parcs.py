import numpy as np
import nibabel as nib
import os

from helpers import conv_to_array_32k_space, conv_matlab, merge

def main():

    # Load from gordon_balsa
    gordon = conv_to_array_32k_space('raw/gordon_balsa/Gordon333_FreesurferSubcortical.32k_fs_LR.dlabel.nii')
    np.save('parcels/gordon.npy', gordon)
    brodmann = conv_to_array_32k_space('raw/gordon_balsa/Human.Brodmann09.32k_fs_LR.dlabel.nii')
    np.save('parcels/brodmann.npy', brodmann)
    vdg11b = conv_to_array_32k_space('raw/gordon_balsa/Human.Composite_VDG11.32k_fs_LR.dlabel.nii')
    np.save('parcels/vdg11b.npy', vdg11b)

    # Load hcp_mmp_balse
    lh = conv_to_array_32k_space('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    rh = conv_to_array_32k_space('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii')
    hcp_mmp = merge(lh, rh)
    np.save('parcels/hcp_mmp.npy', hcp_mmp)

    # Unpack arslan box
    lh_map = nib.load('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.L.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]
    rh_map = nib.load('raw/hcp_mmp_balsa/Q1-Q6_RelatedParcellation210.R.CorticalAreas_dil_Colors.32k_fs_LR.dlabel.nii').header.get_index_map(1)[0]

    a_dr = 'raw/arslan_box/'
    parcs = os.listdir(a_dr)
    for parc in parcs:
        base = os.path.join(a_dr, parc, parc)
        lh_loc, rh_loc = base + '_L.mat', base + '_R.mat'
        data = conv_matlab(lh_loc, rh_loc, lh_map, rh_map)
        np.save('parcels/' + parc.lower() + '_abox', data)

    # Unpack diedrichsen_lab parcels
    dr = 'raw/diedrichsen_lab/'
    parcs = os.listdir(dr)
    parcs = set([p.replace('.R.', '.L.') for p in parcs])

    for p in parcs:
        loc = os.path.join(dr, p)
        lh = conv_to_array_32k_space(loc)
        rh = conv_to_array_32k_space(loc.replace('.L.', '.R.'))
        data = merge(lh, rh)
        np.save('parcels/' + p.split('.')[0].lower() + '_dlab.npy', data)


    # Unpack schaefer
    for size in range(100, 1001, 100):
        loc = 'raw/schaefer_cifti/Schaefer2018_' + str(size) + 'Parcels_7Networks_order.dscalar.nii'
        data = conv_to_array_32k_space(loc)
        np.save('parcels/schaefer_' + str(size), data)

if __name__ == "__main__":
    main()