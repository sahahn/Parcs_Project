from sklearn.linear_model import ElasticNetCV
from BPt.extensions import SurfLabels
from BPt import Model, Model_Pipeline, Scaler, Loader, Param_Search, Feat_Selector


def get_pipe(model_str, parcel, cv=None, dask_ip=None):

    print('Get pipeline with:', model_str,
           parcel, cv, dask_ip, flush=True)

    # Define loader with cache
    rois = SurfLabels(labels='/users/s/a/sahahn/Parcs_Project/parcels/' + parcel + '.npy')
    loader = Loader(rois, cache_loc='/users/s/a/sahahn/scratch/cache3/' + parcel)

    base_param_search =\
        Param_Search(search_type='RandomSearch', n_iter=60,
                     splits=3, n_repeats=1, cv=cv, dask_ip=dask_ip)


    if model_str == 'elastic':

        model = Model('elastic', params=1,
                      param_search=base_param_search,
                      extra_params={'tol': 1e-3})

    elif model_str == 'lgbm':

        lgbm_param_search =\
            Param_Search(search_type='TwoPointsDE', n_iter=180,
                         splits=0.25, n_repeats=1, cv=cv, dask_ip=dask_ip)

        model = Model('light gbm', params=1, param_search=lgbm_param_search)

    elif model_str == 'svm':

        feat_selector =\
            Feat_Selector('univariate selection', params=2)

        nested_svm_pipe =\
            Model_Pipeline(imputers=None,
                           feat_selectors=feat_selector,
                           model=Model('svm', params=1),
                           param_search=base_param_search)

        model = Model(nested_svm_pipe)

    else:
        model = None
    
    # Wrap in pipeline
    pipeline = Model_Pipeline(imputers=None,
                              loaders = loader,
                              scalers = Scaler('robust'),
                              model = model)
    
    return pipeline
