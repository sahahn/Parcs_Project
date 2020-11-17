import nibabel as nib
import numpy as np
from scipy.io import loadmat
from nibabel import GiftiImage

from nilearn.surface import load_surf_mesh, load_surf_data
import numpy as np
import networkx as nx
import os

def load_geo(standard_mesh_loc):

    lh_loc = os.path.join(standard_mesh_loc, 'L.sphere.32k_fs_LR.surf.gii')
    rh_loc = os.path.join(standard_mesh_loc, 'R.sphere.32k_fs_LR.surf.gii')

    lh = load_surf_mesh(lh_loc)[1]
    rh = load_surf_mesh(rh_loc)[1]

    rh += (np.max(lh) + 1)
    raw_geo = np.concatenate([lh, rh])
    
    G = nx.Graph()
    for tri in raw_geo:
        G.add_edge(tri[0], tri[1])
        G.add_edge(tri[0], tri[2])
        G.add_edge(tri[1], tri[2])
        
    geo = []
    for i in range(len(G)):
        geo.append(list(G.neighbors(i)))
    
    return geo

def load_medial_wall(annot_loc):
    
    medial_wall = load_surf_data(annot_loc)
    medial_wall_mask = ~medial_wall.astype('bool')

    return medial_wall_mask

def merge(lh, rh):
    
    ul = np.unique(lh)
    ur = np.unique(rh)
    intersect = len(np.intersect1d(ul, ur))
    
    if intersect > 0:
        if intersect / len(ul) > .75:

            # Add max + 1, since parcs can start at 0
            rh += (max(ul) + 1)
        
    data = np.concatenate([lh, rh])
    return data

def extract(surf, data):
    
    to_fill = np.zeros(surf.surface_number_of_vertices)
    verts = data[surf.index_offset:surf.index_offset + surf.index_count]
    to_fill[surf.vertex_indices._indices] = verts
    
    return to_fill

def conv_to_array_32k_space(data_loc):
    
    raw = nib.load(data_loc)
    
    # Check if GiftiImage
    if isinstance(raw, GiftiImage):
        data = raw.darrays[0].data

        if data.shape == (32492,):
            return data
        else:
            print('GIFTI found with shape', data.shape)

    data = raw.get_fdata().squeeze()
    
    index_map = raw.header.get_index_map(1) 
    shape = data.shape[0]
    
    if shape == 91282:
        
        lh_surf = index_map[1]
        rh_surf = index_map[2]
        
        lh = extract(lh_surf, data)
        rh = extract(rh_surf, data)
        
        return merge(lh, rh)
        
    elif shape == 64984 or shape == 59412:
        
        lh_surf = index_map[0]
        rh_surf = index_map[1]
        
        lh = extract(lh_surf, data)
        rh = extract(rh_surf, data)
        
        return merge(lh, rh)
    
    elif shape == 29696 or shape == 32492 or shape == 29716:
        
        surf = index_map[0]
        return extract(surf, data)
    
    else: 
        print('Warning shape =', shape)

def conv_matlab(lh_loc, rh_loc, lh_map, rh_map):

    lh_d = loadmat(lh_loc)['parcels'].squeeze()
    rh_d = loadmat(rh_loc)['parcels'].squeeze()

    lh = extract(lh_map, lh_d)
    rh = extract(rh_map, rh_d)

    return merge(lh, rh)

def extract_rois(loc):
    
    if loc.split('/')[-1].startswith('rh'):
        prepend = 'rh.'
    else:
        prepend = 'lh.'
    
    header = None
    with open(loc, 'r') as f:
        d = {}
        
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('# ColHeaders'):
                header = line.replace('# ', '')
                header = header.split(' ')[2:]
            if not line.startswith('#'):
                line = [l for l in line.split() if len(l) > 0]
                feat = line[0]
                values = line[1:]
                for i in range(len(values)):
                    nm = prepend + feat+'_'+header[i]
                    d[nm.lower()] = values[i]
        return d

def surf_to_surf(in_loc, hemi, cmd_type='-metric-resample'):
    '''Or cmd_type as -label-resample, don't think will be used though'''
    
    cwd = os.getcwd()

    # Convert to correct space
    std_mesh_dr = '/home/sage/Parcs_Project/raw/standard_mesh_atlases/'
    r_dr = os.path.join(std_mesh_dr, 'resample_fsaverage')
    
    output_loc = os.path.join(cwd, hemi + '.temp.label.gii')

    cmd = 'wb_command ' + cmd_type + ' '
    cmd += in_loc + ' '
    cmd += os.path.join(r_dr, 'fsaverage_std_sphere.' + hemi + '.164k_fsavg_' + hemi + '.surf.gii') + ' '
    cmd += os.path.join(r_dr, 'fs_LR-deformed_to-fsaverage.' + hemi + '.sphere.32k_fs_LR.surf.gii') + ' '
    cmd += 'ADAP_BARY_AREA '
    cmd += output_loc + ' '
    cmd += '-area-metrics '
    cmd += os.path.join(r_dr, 'fsaverage.' + hemi + '.midthickness_va_avg.164k_fsavg_' + hemi + '.shape.gii') + ' '
    cmd += os.path.join(r_dr, 'fs_LR.' + hemi + '.midthickness_va_avg.32k_fs_LR.shape.gii')
    
    os.system(cmd)
    return output_loc

def volume_to_surf(vol):
    
    cwd = os.getcwd()

    temp_name = 'temp'
    in_file_loc = os.path.join(cwd, temp_name + '.nii')
    
    # Save temp as input
    nib.save(vol, in_file_loc)

    matlab_bin = '/home/sage/Downloads/matlab/bin'
    conv_script_loc = '/home/sage/CBIG/stable_projects/registration/Wu2017_RegistrationFusion/bin/standalone_scripts_for_MNI_fsaverage_projection/CBIG_RF_projectMNI2fsaverage.sh'

    cmd = 'bash ' + conv_script_loc + ' -s ' + in_file_loc + ' -o ' + cwd + ' -m ' + matlab_bin

    # Run the command
    os.system(cmd)
    os.remove(in_file_loc)

    ext = '.allSub_RF_ANTs_MNI152_orig_to_fsaverage.nii.gz'
    lh_loc = os.path.join(cwd, 'lh.' + temp_name + ext)
    rh_loc = os.path.join(cwd, 'rh.' + temp_name + ext)
    
    # Need to convert to gifti
    fs_cmd = 'source /home/sage/Downloads/freesurfer/SetUpFreeSurfer.sh'
    
    lh_gifti = 'L.' + temp_name + '.gii'
    rh_gifti = 'R.' + temp_name + '.gii'

    # Write full command to temp file and run
    with open('temp.sh', 'w') as f:
        f.write(fs_cmd + ' && ')
        f.write('mri_convert ' + lh_loc + ' ' + lh_gifti + ' && ')
        f.write('mri_convert ' + rh_loc + ' ' + rh_gifti)

    os.system('bash temp.sh')
    os.remove('temp.sh')
    os.remove(lh_loc)
    os.remove(rh_loc)
    
    # Convert to correct spaces
    lh_loc = surf_to_surf(lh_gifti, 'L', '-metric-resample')
    rh_loc = surf_to_surf(rh_gifti, 'R', '-metric-resample')
    os.remove(lh_gifti)
    os.remove(rh_gifti)
    
    lh = load_surf_data(lh_loc)
    rh = load_surf_data(rh_loc)
    
    os.remove(lh_loc)
    os.remove(rh_loc)
    
    return lh, rh

def vol_labels_to_surf(vol):
    
    data = vol.get_fdata()
    unique_parcels = np.unique(data)
    surfs = []

    for u in unique_parcels:
        temp = np.zeros(data.shape)
        temp[data == u] = 1
        temp_as_vol = nib.Nifti1Image(temp, affine=vol.affine)

        lh, rh = volume_to_surf(temp_as_vol)
        surfs.append(np.concatenate([lh, rh]))

    surfs = np.array(surfs)
    
    return np.argmax(surfs, axis=0)

def prob_vol_labels_to_surf(vol):
    
    data = vol.get_fdata()
    surfs = []
    
    for i in range(data.shape[-1]):
        temp_as_vol = nib.Nifti1Image(data[:,:,:,i], affine=vol.affine)
        
        try:
            lh, rh = volume_to_surf(temp_as_vol)
        except:

            for x in range(100):
                print(i)
                
            continue
        
        # Only add if not all 0's
        if not ((lh == 0).all() and (rh == 0).all()):
            surfs.append(np.concatenate([lh, rh]))
    
    # Return as vertex by maps
    return np.swapaxes(np.array(surfs), 0, 1)