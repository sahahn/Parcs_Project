from BPt.extensions import SurfLabels, SurfMaps
from BPt import (Model, Model_Pipeline, Scaler,
                 Loader, Param_Search, Feat_Selector,
                 CV_Splits, Ensemble)
import numpy as np
import nevergrad as ng

cache_dr = '/users/s/a/sahahn/scratch/cache1/'

def get_base_parcel_names(parcel):

    # Either range or fixed
    parcel_size = parcel.split('_')[2]
    
    # Get number of parcels and the random seed
    n_parcels = int(parcel.split('_')[3])
    parcel_seed = int(parcel.split('_')[4])

    # If parcel size is a range
    if '-' in parcel_size:
        min_size = int(parcel_size.split('-')[0])
        max_size = int(parcel_size.split('-')[1])
        
        # Generate sizes as points between either end,
        # including either end.
        sizes = np.linspace(min_size, max_size, n_parcels).astype('int')
        base_parcels = ['random_' + str(size) + '_' + str(parcel_seed) for size in sizes]

    # Or fixed
    else:
        parcel_size = int(parcel_size)
    
        # If fixed, then we want the starting random parcel to be
        # the maximum size (10) * the parcel seed. So that each repeat between
        # n_parcels == 3 and say 5 is comparable, but so that repeat 2 for 
        # parcels == 3 doesn't overlap with repeat 1's last two parcels in 5 parcels.
        start = int(10 * parcel_seed)
        end = start + n_parcels
        base_parcels = ['random_' + str(parcel_size) + '_' + str(n) for n in range(start, end)]

    return base_parcels

def get_random_grid(model_str, parcel, cv=None, dask_ip=None):

    # Get the base parcel names
    base_parcels = get_base_parcel_names(parcel)

    # Wrap each name in the full path to extra rand. parcels
    parcel_locs = ['../extra_random_parcels/' + p + '.npy' for p in base_parcels]

    # Create the loader with SurfLabels Obj, and as hyperparams the choice of parcel
    loader = Loader(obj=SurfLabels(labels=parcel_locs[0]),
                    params={'labels': ng.p.Choice(parcel_locs)}, 
                    cache_loc=cache_dr + parcel)

    # Get base model, w/ nested param search
    model = get_base_model(model_str=model_str, cv=cv,
                           dask_ip=dask_ip, memmap_X=False,
                           svm_cache_size=1000)


    # Make the pipeline w/ grid search over choice of parcellation
    pipeline = Model_Pipeline(imputers=None,
                              loaders=loader,
                              model=model,
                              scalers=Scaler('robust'),
                              param_search=Param_Search('grid'))

    return pipeline

def get_ensemble_base_models(model_str, parcel, cv=None, dask_ip=None):
    
    # Get the base parcel names
    base_parcels = get_base_parcel_names(parcel)
    
    # Use the parcels to get a full model for each
    base_models = [Model(get_pipe(model_str, p,
                                  cv, dask_ip,
                                  ensemble=parcel)) for p in base_parcels]
    
    return base_models

def get_random_voted(model_str, parcel, cv=None, dask_ip=None):

    # Get base models
    base_models = get_ensemble_base_models(model_str=model_str,
                                           parcel=parcel, cv=cv,
                                           dask_ip=dask_ip)
    
    # Create voting ensemble
    voting_ensemble = Ensemble(obj = "voting",
                               models = base_models,
                               n_jobs_type = 'models')
    
    # Wrap in pipeline
    pipeline = Model_Pipeline(imputers=None,
                              model=voting_ensemble)
    
    return pipeline

def get_random_stacked(model_str, parcel, cv=None, dask_ip=None):

    # Set the outer combining model
    stack_param_search = Param_Search(search_type='RandomSearch',
                                      n_iter=60,
                                      splits=3,
                                      n_repeats=1)
    stack_model = Model('ridge', params=1, param_search=stack_param_search)

    # Only do an internal 3-fold CV for generating predictions for stacking
    stack_splits = CV_Splits(cv=cv, splits=3, n_repeats=1)

    # Get base models
    base_models = get_ensemble_base_models(model_str=model_str,
                                           parcel=parcel, cv=cv,
                                           dask_ip=dask_ip)
    # Create the stacking ensemble
    stacking_ensemble = Ensemble(obj = "stacking",
                                 models = base_models,
                                 cv_splits = stack_splits,
                                 base_model = stack_model,
                                 n_jobs_type = 'models')

    # Wrap in pipeline
    pipeline = Model_Pipeline(imputers=None,
                              model=stacking_ensemble)

    return pipeline

def get_base_model(model_str, cv, dask_ip, memmap_X=False, svm_cache_size=1500):

    base_param_search =\
        Param_Search(search_type='RandomSearch', n_iter=60,
                     splits=3, n_repeats=1, cv=cv, dask_ip=dask_ip,
                     memmap_X=memmap_X)

    if model_str == 'elastic':

        model = Model('elastic', params=1,
                      param_search=base_param_search,
                      extra_params={'tol': 1e-3})

    elif model_str == 'lgbm':

        lgbm_param_search =\
            Param_Search(search_type='TwoPointsDE', n_iter=180,
                         splits=0.25, n_repeats=1, cv=cv,
                         dask_ip=dask_ip, memmap_X=memmap_X)

        model = Model('light gbm', params=1, param_search=lgbm_param_search)

    elif model_str == 'svm':

        # Use a feat selector with variance threshopld and univariate selection
        feat_selector =\
            [Feat_Selector('variance threshold'),
             Feat_Selector('univariate selection', params=2)]

        # For svm param search add special search only parameter
        base_param_search.search_only_params = {'svm classifier__probability': False}
        
        # Create nested SVM
        nested_svm_pipe =\
            Model_Pipeline(imputers=None,
                           feat_selectors=feat_selector,
                           model=Model('svm', params=1, extra_params={'cache_size': svm_cache_size}),
                           param_search=base_param_search)

        model = Model(nested_svm_pipe)

    else:
        model = None

    return model

def get_pipe(model_str, parcel, cv=None, dask_ip=None, ensemble=None):

    print('Get pipeline with:', model_str,
           parcel, cv, dask_ip, flush=True)

    # Nested check for stacked random
    if parcel.startswith('stacked_random'):
        return get_random_stacked(model_str, parcel, cv=cv, dask_ip=dask_ip)
    elif parcel.startswith('voted_random'):
        return get_random_voted(model_str, parcel, cv=cv, dask_ip=dask_ip)
    elif parcel.startswith('grid_random'):
        return get_random_grid(model_str, parcel, cv=cv, dask_ip=dask_ip)

    # Default svm cache size of lets try 1gb
    svm_cache_size = 1000
    memmap_X = False

    # For no parcel / loader
    if parcel == '':
        loader = None

    # For identity loader
    elif parcel == 'identity':

        # Fix number of jobs at 1
        loader = Loader('identity', fix_n_wrapper_jobs=1)

        # Try 16gb cache size for identity
        svm_cache_size = 16000
        memmap_X = True
    
    # Set as either SurfMaps or SurfLabels, depending on type of parcel / map
    else:

        # If not a sub ensemble model
        if ensemble is None:
            parc_loc = '../parcels/' + parcel + '.npy'
            cache_loc = cache_dr + parcel

        # Otherwise, the name of the base ensemble model,
        # e.g., stacked_random_100_3_0 is passed as ensemble
        else:
            parc_loc = '../extra_random_parcels/' + parcel + '.npy'
            cache_loc = cache_dr + ensemble + '/' + parcel

        if len(np.load(parc_loc).shape) == 2:
            rois = SurfMaps(maps=parc_loc)
        else:
            rois = SurfLabels(labels=parc_loc)

        loader = Loader(rois, cache_loc=cache_loc)

    # Get base model
    model = get_base_model(model_str, cv, dask_ip,
                           memmap_X=memmap_X,
                           svm_cache_size=svm_cache_size)
    
    # Wrap in pipeline
    pipeline = Model_Pipeline(imputers=None,
                              loaders=loader,
                              scalers=Scaler('robust'),
                              model=model)
    
    return pipeline
