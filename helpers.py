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