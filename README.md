# Parcellation Project

It is common to analyze surface-based neuroimaging data, and likewise for a number of reasons to reduce surface data to a collection of representative regions of interest. What about when one is interested in performing machine learning? Is there a best pre-defined parcellation to use? This project seeks to answer that question.

The base experiment conducted within this project is a systematic test of different pre-defined parcellations performance. There are some key decision though which greatly influence the experiment.

-----

### Directory structure

This project is setup with a few different directories. In general those starting with capital letters, (Setup/, Exp/, Plots/) contain code used to run different steps, where lowercase directories are for data (data/, parcels/, ect...).

-----

### Input Data

Data from the ABCD Study release 2, NDA Collection 3165 (See: https://collection3165.readthedocs.io/en/stable/). Data used within this study are the sMRI outputs of a modified HCP style pipeline. We downloaded for each available subject their left and right hemisphere curvature, sulcal depth, cortical thickness and unsmoothed myelin map, each in the standard FS LR 32k vertex space. Likewise, we additionally downloaded each subject's automatically computed FreeSurfer ROI stats files. 

We chose to use structural MRI surfaces. That said, the idea of parcellations easily extends to task-based fMRI and resting state fMRI just as easily as dMRI. The choice to use structural MRI surfaces was therefore somewhat arbitrary, but given its ubiquity and the amount of avaliable studies which employ it, it may not be a bad choice. That said, future work may very well consider different modalities or explicitly multi-modal fusion.

----

### Target Variables

A collection of 45 target phenotypic variables (23 binary and 22 continuous), used to gauge predictive performance, was sourced from the second ABCD Study release. Variables were sourced directly from the rds file made available by the DAIRC (specifically on a version of the rds file saved as a csv). All collected variables, both target and brain, are from the baseline time point on the study. Best efforts were made to source a list of representative, diverse and predictive variables. Towards this effort, a larger list of variables was originally screened on a subset of the data (n=2000) to avoid including variables not at all predictive from sMRI measures. 

See [setup_ML_Logs/Exp/](https://github.com/sahahn/Parcs_Project/tree/main/Setup/setup_ML_Logs/My_Exp) whichlists all target variables used and shows their distribution.

----

### Parcellations

All considered surface parcellations were converted, if necessary, in the FS LR 32K standard left and right hemisphere standard vertex space. We consider two main sources for surface parcellations, existing and random. Lastly, a few additional variants are tested including downsampled and as extracted directly from FreeSurfer.


This project uses the idea of random surface parcellations extensively. Random parcellations are generated as follows: For a random parcellation of size N, N random points are first selected at random across both hemisphere’s 59,412 vertices (medial wall vertices excluded). Each selected point is then assigned as the seed of a new region and is randomly assigned a size probability between 0 and 1. Next, a region is randomly selected according to a weighted random choice between all regions (e.g., if a region was assigned an initial probability of .5 it would be picked on average twice as often as a region assigned .25). A random vertex is then added to the selected region from the list of valid neighboring unassigned vertices. This sequence, of selecting a region and adding one valid vertex, is repeated until all regions have no unassigned neighbors and therefore all non-medial wall vertices are assigned to a region. 


Example generated random parcellation:

<img width="500em" src="https://raw.githubusercontent.com/sahahn/Parcs_Project/master/data/rand_parc.gif"/>

Note: The above example, in contrast to the random parcellations generated in this project, is in fsaverage5 space (vs. fs_LR_32k) and doesn't mask the medial wall (the medial wall is masked in this project).

Source code for generating random parcellations is implemented and avaliable through the Brain Predictability toolbox (BPt) at https://github.com/sahahn/BPt/blob/master/BPt/extensions/RandomParcels.py. In this project, random parcels are generated within Setup/process_random_parcels.py script.

----

### Machine Learning (ML)

We employ three base ML pipelines, each with classifier and regressor variants, as a representative sample of different popular and predictive ML strategies. All machine learning experiments are conducted with BPt. Each pipeline is first composed of a loading component responsible for extracting ROIs according to the specified surface parcellation. The output from the loading step concatenates the extracted ROI values across each of the different surface values, generating a feature vector of length four times the number of parcels for each subject. Next, the ROI values are scaled using robust scaling, where each feature is standardized by first removing the median and then scaling according to the 5th and 95th percentiles of that features distribution. These features are then used as input to train a classifier or regressor under one of three different base configurations, these are:


#### Elastic-Net
The base model within the pipeline under this configuration is a logistic or linear regression with elastic-net penalty available from scikit-learn. A nested random hyper-parameter search over 60 combinations is evaluated through nested 3-fold CV to select the strength of regularization applied as well as the ratio between l1 and l2 regularization.

    param_search = Param_Search(search_type='RandomSearch', n_iter=60,
                                splits=3, n_repeats=1, cv=cv)

    model = Model('elastic', params=1,
                  param_search=param_search,
                  extra_params={'tol': 1e-3})

#### SVM
The base model within the pipeline under this configuration is a Support Vector Machine (SVM) classifier or regressor with radial basis function kernel available from scikit-learn. A front end univariate feature selection procedure was further added to this pipeline configuration (based on the ANOVA f-value between a feature and the target variable). A nested random hyper-parameter search over 60 combinations is then evaluated through nested 3-fold CV in order to select the SVM’s strength of regularization and kernel coefficient as well as the percent of features to keep in the front-end feature selector. All three hyper-parameters are optimized at the same time.

    param_search = Param_Search(search_type='RandomSearch', n_iter=60,
                                splits=3, n_repeats=1, cv=cv,
                                search_only_params={'svm classifier__probability': False})

    feat_selector =\
            [Feat_Selector('variance threshold'),
             Feat_Selector('univariate selection', params=2)]

    nested_svm_pipe =\
        Model_Pipeline(feat_selectors=feat_selector,
                       model=Model('svm', params=1, extra_params={'cache_size': 2000}),
                       param_search=param_search)

    model = Model(nested_svm_pipe)


#### LGBM
The base model optimized is an extreme gradient boosted tree based classifier and regressor from the Light Gradient Boosting Machine (LGBM) package. The tuned hyper-parameters for this model included the type of boosting, the number of estimators, different tree sampling parameters, and regularization parameters. Given the high number of hyper-parameters to tune, 9, in contrast to the other base models, we employed a two point differential evolution based hyper-parameter search strategy implemented through the python library Nevergrad. The search was run for 180 iterations, where each set of parameters is evaluated with a single 25% nested validation split.


    lgbm_param_search =\
            Param_Search(search_type='TwoPointsDE', n_iter=180,
                         splits=0.25, n_repeats=1, cv=cv)

    model = Model('light gbm', params=1, param_search=lgbm_param_search)

----
