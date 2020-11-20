from BPt.extensions import SurfLabels
from BPt import (Model, Model_Pipeline, Scaler,
                 Loader, Param_Search, Feat_Selector,
                 CV_Splits, Ensemble)


def get_random_stacked(model_str, parcel, cv=None, dask_ip=None):

    stack_param_search = Param_Search(search_type='RandomSearch',
                                      n_iter=60,
                                      splits=3,
                                      n_repeats=1)
    stack_model = Model('ridge', params=1, param_search=stack_param_search)

    stack_splits = CV_Splits(cv=cv, splits=5, n_repeats=1)

    parcel_size = parcel.split('_')[2]
    n_parcels = int(parcel.split('_')[3])
    parcel_seed = int(parcel.split('_')[4])

    start = int(n_parcels * parcel_seed)
    end = start + n_parcels
    base_parcels = ['random_' + parcel_size + '_' + str(n) for n in range(start, end)]
    
    base_models = [Model(get_pipe(model_str, p, cv, dask_ip)) for p in base_parcels]

    stacking_ensemble = Ensemble(obj = "stacking regressor",
                                 models = base_models,
                                 cv_splits = stack_splits,
                                 base_model = stack_model,
                                 n_jobs_type = 'models')

    pipeline = Model_Pipeline(imputers=None,
                              model=stacking_ensemble)

    return pipeline


def get_pipe(model_str, parcel, cv=None, dask_ip=None):

    print('Get pipeline with:', model_str,
           parcel, cv, dask_ip, flush=True)

    if parcel.startswith('stacked_random'):
        return get_random_stacked(model_str, parcel, cv=cv, dask_ip=dask_ip)

    # Define loader with cache
    rois = SurfLabels(labels='/users/s/a/sahahn/Parcs_Project/parcels/' + parcel + '.npy')
    loader = Loader(rois, cache_loc='/users/s/a/sahahn/scratch/cache1/' + parcel)

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
            [Feat_Selector('variance threshold'),
             Feat_Selector('univariate selection', params=2)]

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
                              loaders=loader,
                              scalers=Scaler('robust'),
                              model=model)
    
    return pipeline
