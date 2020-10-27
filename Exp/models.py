from sklearn.linear_model import ElasticNetCV
from BPt.extensions import SurfLabels
from BPt import Model, Model_Pipeline, Scaler, Loader, Param_Search


def get_pipe(model_str, parcel, cv=None, dask_ip=None):

    print('Get pipeline with:', model_str,
           parcel, cv, dask_ip, flush=True)

    # Define loader with cache
    rois = SurfLabels(labels='/users/s/a/sahahn/Parcs_Project/parcels/' + parcel + '.npy')
    loader = Loader(rois, cache_loc='/users/s/a/sahahn/scratch/cache/' + parcel)


    if model_str == 'elastic':
        model = Model(ElasticNetCV(max_iter=3000,
                                   tol=1e-3,
                                   selection='random',
                                   verbose=0))

    elif model_str == 'lgbm':

        lgbm_param_search =\
            Param_Search(search_type='TwoPointsDE', n_iter=200,
                         splits=0.2, n_repeats=1, CV=cv)

        model = Model('light gbm', params=1, param_search=lgbm_param_search)


    else:
        model = None
    
    # Wrap in pipeline
    pipeline = Model_Pipeline(loaders = loader,
                              scalers = Scaler('robust'),
                              model = model)
    
    return pipeline
