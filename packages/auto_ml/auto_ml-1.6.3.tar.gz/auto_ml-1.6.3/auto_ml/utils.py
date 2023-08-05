from collections import OrderedDict
import csv
import datetime
import dateutil
import math
import os
import random

# from keras.constraints import maxnorm
# from keras.layers import Dense, Dropout
# from keras.models import Sequential
# from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor, AdaBoostRegressor, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.feature_selection import GenericUnivariateSelect, RFECV, SelectFromModel
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import RandomizedLasso, RandomizedLogisticRegression, RANSACRegressor, LinearRegression, Ridge, Lasso, ElasticNet, LassoLars, OrthogonalMatchingPursuit, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor, LogisticRegression, RidgeClassifier, SGDClassifier, Perceptron, PassiveAggressiveClassifier
from sklearn.metrics import mean_squared_error, make_scorer, brier_score_loss, accuracy_score, explained_variance_score, mean_absolute_error, median_absolute_error, r2_score
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
import pandas as pd
import pathos
import scipy

# XGBoost can be a pain to install. It's also a super powerful and effective package.
# So we'll make it optional here. If a user wants to install XGBoost themselves, we fully support XGBoost!
# But, if they just want to get running out of the gate, without dealing with any installation other than what's done for them automatically, we won't force them to go through that.
# The same logic will apply to deep learning with Keras and TensorFlow
global xgb_installed
xgb_installed = False
try:
    import xgboost as xgb
    xgb_installed = True
except NameError:
    pass
except ImportError:
    pass

if xgb_installed:
    import xgboost as xgb


# The easiest way to check against a bunch of different bad values is to convert whatever val we have into a string, then check it against a set containing the string representation of a bunch of bad values
bad_vals_as_strings = set([str(float('nan')), str(float('inf')), str(float('-inf')), 'None', 'none', 'NaN', 'nan', 'NULL', 'null', '', 'inf', '-inf'])

# clean_val will try to turn a value into a float.
# If it fails, it will attempt to strip commas and then attempt to turn it into a float again
# Additionally, it will check to make sure the value is not in a set of bad vals (nan, None, inf, etc.)
# This function will either return a clean value, or raise an error if we cannot turn the value into a float or the value is a bad val
def clean_val(val):
    if str(val) in bad_vals_as_strings:
        raise(ValueError('clean_val failed'))
    else:
        try:
            float_val = float(val)
        except:
            # This will throw a ValueError if it fails
            # remove any commas in the string, and try to turn into a float again
            cleaned_string = val.replace(',', '')
            float_val = float(cleaned_string)
        return float_val

# Same as above, except this version returns float('nan') when it fails
# This plays more nicely with df.apply, and assumes we will be handling nans appropriately when doing DataFrameVectorizer later.
def clean_val_nan_version(val):
    if str(val) in bad_vals_as_strings:
        return float('nan')
    else:
        try:
            float_val = float(val)
        except:
            # This will throw a ValueError if it fails
            # remove any commas in the string, and try to turn into a float again
            cleaned_string = val.replace(',', '')
            try:
                float_val = float(cleaned_string)
            except:
                return float('nan')
        return float_val


# Hyperparameter search spaces for each model
def get_search_params(model_name):
    grid_search_params = {
        # 'DeepLearningRegressor': {
        #     # 'shape': ['triangle_left', 'triangle_right', 'triangle_cuddles', 'long', 'long_and_wide', 'standard']
        #     'dropout_rate': [0.0, 0.2, 0.4, 0.6, 0.8]
        #     , 'weight_constraint': [0, 1, 3, 5]
        #     , 'optimizer': ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
        # },
        'XGBClassifier': {
            'max_depth': [1, 3, 5, 10],
            'learning_rate': [0.01, 0.1, 0.2],
            'min_child_weight': [1, 5, 10],
            # 'subsample': [0.5, 1.0]
            'subsample': [0.5, 0.8, 1.0],
            'colsample_bytree': [0.5, 0.8, 1.0]
            # 'lambda': [0.9, 1.0]
        },
        'XGBRegressor': {
            # Add in max_delta_step if classes are extremely imbalanced
            'max_depth': [1, 3, 8, 25],
            # 'lossl': ['ls', 'lad', 'huber', 'quantile'],
            # 'booster': ['gbtree', 'gblinear', 'dart'],
            # 'objective': ['reg:linear', 'reg:gamma'],
            # 'learning_rate': [0.01, 0.1],
            'subsample': [0.5, 1.0]
            # 'subsample': [0.4, 0.5, 0.58, 0.63, 0.68, 0.76],

        },
        'GradientBoostingRegressor': {
            # Add in max_delta_step if classes are extremely imbalanced
            'max_depth': [1, 2, 3, 5],
            'max_features': ['sqrt', 'log2', None],
            # 'loss': ['ls', 'lad', 'huber', 'quantile']
            # 'booster': ['gbtree', 'gblinear', 'dart'],
            # 'loss': ['ls', 'lad', 'huber'],
            'loss': ['ls', 'huber'],
            # 'learning_rate': [0.01, 0.1, 0.25, 0.4, 0.7],
            'subsample': [0.5, 0.8, 1.0]
        },
        'GradientBoostingClassifier': {
            'loss': ['deviance', 'exponential'],
            'max_depth': [1, 2, 3, 5],
            'max_features': ['sqrt', 'log2', None],
            # 'learning_rate': [0.01, 0.1, 0.25, 0.4, 0.7],
            'subsample': [0.5, 1.0]
            # 'subsample': [0.4, 0.5, 0.58, 0.63, 0.68, 0.76]

        },

        'LogisticRegression': {
            'C': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'class_weight': [None, 'balanced'],
            'solver': ['newton-cg', 'lbfgs', 'sag']
        },
        'LinearRegression': {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        },
        'RandomForestClassifier': {
            'criterion': ['entropy', 'gini'],
            'class_weight': [None, 'balanced'],
            'max_features': ['sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'RandomForestRegressor': {
            'max_features': ['auto', 'sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'RidgeClassifier': {
            'alpha': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'class_weight': [None, 'balanced'],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']
        },
        'Ridge': {
            'alpha': [.0001, .001, .01, .1, 1, 10, 100, 1000],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag']
        },
        'ExtraTreesRegressor': {
            'max_features': ['auto', 'sqrt', 'log2', None],
            'min_samples_split': [1, 2, 5, 20, 50, 100],
            'min_samples_leaf': [1, 2, 5, 20, 50, 100],
            'bootstrap': [True, False]
        },
        'AdaBoostRegressor': {
            'base_estimator': [None, LinearRegression(n_jobs=-1)],
            'loss': ['linear','square','exponential']
        },
        'RANSACRegressor': {
            'min_samples': [None, .1, 100, 1000, 10000],
            'stop_probability': [0.99, 0.98, 0.95, 0.90]
        },
        'Lasso': {
            'selection': ['cyclic', 'random'],
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'positive': [True, False]
        },

        'ElasticNet': {
            'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9],
            'selection': ['cyclic', 'random'],
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'positive': [True, False]
        },

        'LassoLars': {
            'positive': [True, False],
            'max_iter': [50, 100, 250, 500, 1000]
        },

        'OrthogonalMatchingPursuit': {
            'n_nonzero_coefs': [None, 3, 5, 10, 25, 50, 75, 100, 200, 500]
        },

        'BayesianRidge': {
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'alpha_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_2': [.0000001, .000001, .00001, .0001, .001]
        },

        'ARDRegression': {
            'tol': [.0000001, .000001, .00001, .0001, .001],
            'alpha_1': [.0000001, .000001, .00001, .0001, .001],
            'alpha_2': [.0000001, .000001, .00001, .0001, .001],
            'lambda_1': [.0000001, .000001, .00001, .0001, .001],
            'lambda_2': [.0000001, .000001, .00001, .0001, .001],
            'threshold_lambda': [100, 1000, 10000, 100000, 1000000]
        },

        'SGDRegressor': {
            'loss': ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'learning_rate': ['constant', 'optimal', 'invscaling'],
            'alpha': [.0000001, .000001, .00001, .0001, .001]
        },

        'PassiveAggressiveRegressor': {
            'epsilon': [0.01, 0.05, 0.1, 0.2, 0.5],
            'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'],
            'C': [.0001, .001, .01, .1, 1, 10, 100, 1000],
        },

        'SGDClassifier': {
            'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'],
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'alpha': [.0000001, .000001, .00001, .0001, .001],
            'learning_rate': ['constant', 'optimal', 'invscaling'],
            'class_weight': ['balanced', None]
        },

        'Perceptron': {
            'penalty': ['none', 'l2', 'l1', 'elasticnet'],
            'alpha': [.0000001, .000001, .00001, .0001, .001],
            'class_weight': ['balanced', None]
        },

        'PassiveAggressiveClassifier': {
            'loss': ['hinge', 'squared_hinge'],
            'class_weight': ['balanced', None],
            'C': [0.01, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
        }

    }

    return grid_search_params[model_name]



class BasicDataCleaning(BaseEstimator, TransformerMixin):


    def __init__(self, column_descriptions=None):
        self.column_descriptions = column_descriptions
        self.text_col_indicators = set(['text', 'nlp'])

        self.text_columns = {}
        for key, val in self.column_descriptions.items():
            if val in self.text_col_indicators:
                self.text_columns[key] = TfidfVectorizer(
                    # If we have any documents that cannot be decoded properly, just ignore them and keep going as planned with everything else
                    decode_error='ignore'
                    # Try to strip accents from characters. Using unicode is slightly slower but more comprehensive than 'ascii'
                    , strip_accents='unicode'
                    # Can also choose 'character', which will likely increase accuracy, at the cost of much more space, generally
                    , analyzer='word'
                    # Remove commonly found english words ('it', 'a', 'the') which do not typically contain much signal
                    , stop_words='english'
                    # Convert all characters to lowercase
                    , lowercase=True
                    # Only consider words that appear in fewer than max_df percent of all documents
                    # In this case, ignore all words that appear in 90% of all documents
                    , max_df=0.9
                    # Consider only the most frequently occurring 3000 words, after taking into account all the other filtering going on
                    , max_features=3000
                )

    def fit(self, X_df, y=None):

        # See if we should fit TfidfVectorizer or not
        for key in X_df.columns:
            # col_desc = self.column_descriptions.get(key, False)
            if key in self.text_columns:
                    self.text_columns[key].fit(X_df[key])

        return self

    def transform(self, X, y=None):
        # Convert input to DataFrame if we were given a list of dictionaries
        if isinstance(X, list):
            X = pd.DataFrame(X)

        # All of these are values we will not want to keep for training this particular estimator.
        # Note that we have already split out the output column and saved it into it's own variable
        vals_to_drop = set(['ignore', 'output', 'regressor', 'classifier'])

        # It is much more efficient to drop a bunch of columns at once, rather than one at a time
        cols_to_drop = []

        if isinstance(X, dict):

            dict_copy = {}

            for key, val in X.items():
                col_desc = self.column_descriptions.get(key)

                if col_desc in (None, 'continuous', 'numerical', 'float', 'int'):
                    dict_copy[key] = clean_val_nan_version(val)
                elif col_desc == 'date':
                    date_feature_dict = add_date_features_dict(X, key)
                    dict_copy.update(date_feature_dict)
                elif col_desc == 'categorical':
                    dict_copy[key] = val
                # elif key in self.text_columns:
                    # Add in logic to handle nlp columns here
                elif col_desc in vals_to_drop:
                    pass
                    # del X[key]

        else:
            for key in X.columns:
                col_desc = self.column_descriptions.get(key)
                if col_desc == 'categorical':
                    # We will handle categorical data later, one-hot-encoding it inside DataFrameVectorizer
                    pass

                elif col_desc in (None, 'continuous', 'numerical', 'float', 'int'):
                    # For all of our numerical columns, try to turn all of these values into floats
                    # This function handles commas inside strings that represent numbers, and returns nan if we cannot turn this value into a float. nans are ignored in DataFrameVectorizer
                    X[key] = X[key].apply(clean_val_nan_version)

                elif col_desc == 'date':
                    X = add_date_features_df(X, key)

                elif key in self.text_columns:

                    col_names = self.text_columns[key].get_feature_names()

                    # Make weird characters play nice, or just ignore them :)
                    for idx, word in enumerate(col_names):
                        try:
                            col_names[idx] = str(word)
                        except:
                            col_names[idx] = 'non_ascii_word_' + str(idx)

                    col_names = ['nlp_' + key + '_' + str(word) for word in col_names]

                    nlp_matrix = self.text_columns[key].transform(X[key].values)
                    nlp_matrix = nlp_matrix.toarray()

                    text_df = pd.DataFrame(nlp_matrix)
                    text_df.columns = col_names

                    X = X.join(text_df)
                    # Once the transformed datafrane is added, remove the original text

                    X = X.drop(key, axis=1)

                elif col_desc in vals_to_drop:
                    cols_to_drop.append(key)

                else:
                    # If we have gotten here, the value is not any that we recognize
                    # This is most likely a typo that the user would want to be informed of, or a case while we're developing on auto_ml itself.
                    # In either case, it's useful to log it.
                    print('When transforming the data, we have encountered a value in column_descriptions that is not currently supported. The column has been dropped to allow the rest of the pipeline to run. Here\'s the name of the column:' )
                    print(key)
                    print('And here is the value for this column passed into column_descriptions:')
                    print(col_desc)

        # Historically we've deleted columns here. However, we're moving this to DataFrameVectorizer as part of a broader effort to reduce duplicate computation
        # if len(cols_to_drop) > 0:
        #     X = X.drop(cols_to_drop, axis=1)
        return X


def minutes_into_day_parts(minutes_into_day):
    if minutes_into_day < 6 * 60:
        return 'late_night'
    elif minutes_into_day < 10 * 60:
        return 'morning'
    elif minutes_into_day < 11.5 * 60:
        return 'mid_morning'
    elif minutes_into_day < 14 * 60:
        return 'lunchtime'
    elif minutes_into_day < 18 * 60:
        return 'afternoon'
    elif minutes_into_day < 20.5 * 60:
        return 'dinnertime'
    elif minutes_into_day < 23.5 * 60:
        return 'early_night'
    else:
        return 'late_night'


def add_date_features_df(df, date_col):
    # Pandas nicely tries to prevent you from doing stupid things, like setting values on a copy of a df, not your real one
    # However, it's a bit overzealous in this case, so we'll side-step a bunch of warnings by setting is_copy to false here
    df.is_copy = False

    df[date_col] = pd.to_datetime(df[date_col])
    df[date_col + '_day_of_week'] = df[date_col].apply(lambda x: x.weekday()).astype(int)
    df[date_col + '_hour'] = df[date_col].apply(lambda x: x.hour).astype(int)

    df[date_col + '_minutes_into_day'] = df[date_col].apply(lambda x: x.hour * 60 + x.minute)

    df[date_col + '_is_weekend'] = df[date_col].apply(lambda x: x.weekday() in (5,6))
    df[date_col + '_day_part'] = df[date_col + '_minutes_into_day'].apply(minutes_into_day_parts)

    df = df.drop([date_col], axis=1)

    return df

# Same logic as above, except implemented for a single dictionary, which is much faster at prediction time when getting just a single prediction
def add_date_features_dict(row, date_col):

    date_feature_dict = {}

    # Handle cases where the val for the date_col is None
    try:
        date_val = row[date_col]
        if not isinstance(date_val, (datetime.datetime, datetime.date)):
            date_val = dateutil.parser.parse(date_val)
        if date_val == None:
            return date_feature_dict
    except:
        return date_feature_dict

    # Make a copy of all the engineered features from the date, without modifying the original object at all
    # This way the same original object can be passed into a number of different trained auto_ml predictors


    date_feature_dict[date_col + '_day_of_week'] = date_val.weekday()
    date_feature_dict[date_col + '_hour'] = date_val.hour

    date_feature_dict[date_col + '_minutes_into_day'] = date_val.hour * 60 + date_val.minute

    date_feature_dict[date_col + '_is_weekend'] = date_val.weekday() in (5,6)

    # del row[date_col]

    return date_feature_dict


# TODO: figure out later on how to wrap this inside another wrapper or something to make num_cols more dynamic
# def make_deep_learning_model(num_cols=250, optimizer='adam', dropout_rate=0.2, weight_constraint=0, shape='standard'):
#     model = Sequential()
#     # Add a dense hidden layer, with num_nodes = num_cols, and telling it that the incoming input dimensions also = num_cols
#     model.add(Dense(num_cols, input_dim=num_cols, activation='relu', init='normal', W_constraint=maxnorm(weight_constraint)))
#     model.add(Dropout(dropout_rate))
#     model.add(Dense(num_cols, activation='relu', init='normal', W_constraint=maxnorm(weight_constraint)))
#     model.add(Dense(num_cols, activation='relu', init='normal', W_constraint=maxnorm(weight_constraint)))
#     # For regressors, we want an output layer with a single node
#     # For classifiers, we'll want to add in some other processing here (like a softmax activation function)
#     model.add(Dense(1, init='normal'))

#     # The final step is to compile the model
#     # TODO: see if we can pass in our own custom loss function here
#     model.compile(loss='mean_squared_error', optimizer=optimizer)

#     return model


def get_model_from_name(model_name):
    model_map = {
        # Classifiers
        'LogisticRegression': LogisticRegression(n_jobs=-2),
        'RandomForestClassifier': RandomForestClassifier(n_jobs=-2),
        'RidgeClassifier': RidgeClassifier(),
        'GradientBoostingClassifier': GradientBoostingClassifier(),

        'SGDClassifier': SGDClassifier(n_jobs=-1),
        'Perceptron': Perceptron(n_jobs=-1),
        'PassiveAggressiveClassifier': PassiveAggressiveClassifier(),

        # Regressors
        # 'DeepLearningRegressor': KerasRegressor(build_fn=make_deep_learning_model, nb_epoch=10, batch_size=10, verbose=1),
        'LinearRegression': LinearRegression(n_jobs=-2),
        'RandomForestRegressor': RandomForestRegressor(n_jobs=-2),
        'Ridge': Ridge(),
        'ExtraTreesRegressor': ExtraTreesRegressor(n_jobs=-1),
        'AdaBoostRegressor': AdaBoostRegressor(n_estimators=5),
        'RANSACRegressor': RANSACRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor(presort=False),

        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'LassoLars': LassoLars(),
        'OrthogonalMatchingPursuit': OrthogonalMatchingPursuit(),
        'BayesianRidge': BayesianRidge(),
        'ARDRegression': ARDRegression(),
        'SGDRegressor': SGDRegressor(shuffle=False),
        'PassiveAggressiveRegressor': PassiveAggressiveRegressor(shuffle=False),

        # Clustering
        'MiniBatchKMeans': MiniBatchKMeans(n_clusters=8)
    }
    if xgb_installed:
        model_map['XGBClassifier'] = xgb.XGBClassifier(colsample_bytree=0.8, min_child_weight=5, max_depth=1, subsample=1.0, learning_rate=0.1)
        model_map['XGBRegressor'] = xgb.XGBRegressor()

    return model_map[model_name]


# This is the Air Traffic Controller (ATC) that is a wrapper around sklearn estimators.
# In short, it wraps all the methods the pipeline will look for (fit, score, predict, predict_proba, etc.)
# However, it also gives us the ability to optimize this stage in conjunction with the rest of the pipeline.
# It also gives us more granular control over things like turning the input for GradientBoosting into dense matrices, or appending a set of dummy 1's to the end of sparse matrices getting predictions from XGBoost.
# TODO: make sure we can actually get the params from GridSearchCV.
    # Might have to do something tricky, like have a hold-all function that does nothing but get the params from GridSearchCV inside __init__
        # So, self.model might just be a dictionary or something
        # Or, a function that takes in anything as kwargs, and sets them on a dictionary, then returns that dictionary
    # And then that function does nothing but return those params
    # And we create a model using that inside fit

class FinalModelATC(BaseEstimator, TransformerMixin):


    def __init__(self, model, model_name, X_train=None, y_train=None, ml_for_analytics=False, type_of_estimator='classifier', output_column=None):

        self.model = model
        self.model_name = model_name
        self.X_train = X_train
        self.y_train = y_train
        self.ml_for_analytics = ml_for_analytics
        self.type_of_estimator = type_of_estimator


        if self.type_of_estimator == 'classifier':
            self._scorer = brier_score_loss_wrapper
        else:
            self._scorer = rmse_scoring


    def fit(self, X, y):

        if self.model_name[:3] == 'XGB' and scipy.sparse.issparse(X):
            ones = [[1] for x in range(X.shape[0])]
            # Trying to force XGBoost to play nice with sparse matrices
            X_fit = scipy.sparse.hstack((X, ones))

        else:
            X_fit = X


        # if self.model_name[:12] == 'DeepLearning':
        #     if scipy.sparse.issparse(X_fit):
        #         X_fit = X_fit.todense()

        #     num_cols = X_fit.shape[1]
        #     kwargs = {
        #         'num_cols':num_cols
        #         , 'nb_epoch': 20
        #         , 'batch_size': 10
        #         , 'verbose': 1
        #     }
        #     model_params = self.model.get_params()
        #     del model_params['build_fn']
        #     for k, v in model_params.items():
        #         if k not in kwargs:
        #             kwargs[k] = v
        #     if self.type_of_estimator == 'regressor':
        #         self.model = KerasRegressor(build_fn=make_deep_learning_model, **kwargs)

        self.model.fit(X_fit, y)

        return self


    def score(self, X, y):
        # At the time of writing this, GradientBoosting does not support sparse matrices for predictions
        if self.model_name[:16] == 'GradientBoosting' and scipy.sparse.issparse(X):
            X = X.todense()

        if self._scorer is not None:
            if self.type_of_estimator == 'regressor':
                return self._scorer(self, X, y)
            elif self.type_of_estimator == 'classifier':
                return self._scorer(self, X, y)


        else:
            return self.model.score(X, y)


    def predict_proba(self, X):

        if self.model_name[:3] == 'XGB' and scipy.sparse.issparse(X):
            ones = [[1] for x in range(X.shape[0])]
            # Trying to force XGBoost to play nice with sparse matrices
            X = scipy.sparse.hstack((X, ones))

        if self.model_name[:16] == 'GradientBoosting' and scipy.sparse.issparse(X):
            X = X.todense()

        try:
            return self.model.predict_proba(X)
        except AttributeError:
            # print('This model has no predict_proba method. Returning results of .predict instead.')
            raw_predictions = self.model.predict(X)
            tupled_predictions = []
            for prediction in raw_predictions:
                if prediction == 1:
                    tupled_predictions.append([0,1])
                else:
                    tupled_predictions.append([1,0])
            return tupled_predictions


    def predict(self, X):

        if self.model_name[:3] == 'XGB' and scipy.sparse.issparse(X):
            ones = [[1] for x in range(X.shape[0])]
            # Trying to force XGBoost to play nice with sparse matrices
            X_predict = scipy.sparse.hstack((X, ones))

        elif (self.model_name[:16] == 'GradientBoosting' or self.model_name[:12] == 'DeepLearning') and scipy.sparse.issparse(X):
            X_predict = X.todense()

        else:
            X_predict = X

        prediction = self.model.predict(X_predict)
        # Handle cases of getting a prediction for a single item.
        # It makes a cleaner interface just to get just the single prediction back, rather than a list with the prediction hidden inside.
        if len(prediction) == 1:
            return prediction[0]
        else:
            return prediction


def advanced_scoring_classifiers(probas, actuals):

    print('Here is our brier-score-loss, which is the value we optimized for while training, and is the value returned from .score()')
    print('It is a measure of how close the PROBABILITY predictions are.')
    print(brier_score_loss(actuals, probas))

    print('\nHere is the trained estimator\'s overall accuracy (when it predicts a label, how frequently is that the correct label?)')
    predicted_labels = []
    for pred in probas:
        if pred >= 0.5:
            predicted_labels.append(1)
        else:
            predicted_labels.append(0)
    print(accuracy_score(y_true=actuals, y_pred=predicted_labels))

    print('Here is the accuracy of our trained estimator at each level of predicted probabilities')

    # create summary dict
    summary_dict = OrderedDict()
    for num in range(0, 110, 10):
        summary_dict[num] = []

    for idx, proba in enumerate(probas):
        proba = math.floor(int(proba * 100) / 10) * 10
        summary_dict[proba].append(actuals[idx])

    for k, v in summary_dict.items():
        if len(v) > 0:
            print('Predicted probability: ' + str(k) + '%')
            actual = sum(v) * 1.0 / len(v)

            # Format into a prettier number
            actual = round(actual * 100, 0)
            print('Actual: ' + str(actual) + '%')
            print('# preds: ' + str(len(v)) + '\n')

    print('\n\n')

def calculate_and_print_differences(predictions, actuals):
    pos_differences = []
    neg_differences = []
    # Technically, we're ignoring cases where we are spot on
    for idx, pred in enumerate(predictions):
        difference = pred - actuals[idx]
        if difference > 0:
            pos_differences.append(difference)
        elif difference < 0:
            neg_differences.append(difference)
    print('Count of positive differences (prediction > actual):')
    print(len(pos_differences))
    print('Count of negative differences:')
    print(len(neg_differences))
    print('Average positive difference:')
    print(sum(pos_differences) * 1.0 / len(pos_differences))
    print('Average negative difference:')
    print(sum(neg_differences) * 1.0 / len(neg_differences))
    print('count predictions > 10 min off')
    ten_min_off = [x for x in neg_differences if x < -10 * 60]
    print(len(ten_min_off))
    print('average amount off by for these cases')
    print(sum(ten_min_off) * 1.0 / len(ten_min_off))


def advanced_scoring_regressors(predictions, actuals):

    print('\n\n***********************************************')
    print('Advanced scoring metrics for the trained regression model on this particular dataset:\n')

    # 1. overall RMSE
    print('Here is the overall RMSE for these predictions:')
    print(mean_squared_error(actuals, predictions)**0.5)

    # 2. overall avg predictions
    print('\nHere is the average of the predictions:')
    print(sum(predictions) * 1.0 / len(predictions))

    # 3. overall avg actuals
    print('\nHere is the average actual value on this validation set:')
    print(sum(actuals) * 1.0 / len(actuals))

    # 4. avg differences (not RMSE)
    print('\nHere is the mean absolute error:')
    print(mean_absolute_error(actuals, predictions))

    print('\nHere is the median absolute error (robust to outliers):')
    print(median_absolute_error(actuals, predictions))

    print('\nHere is the explained variance:')
    print(explained_variance_score(actuals, predictions))

    print('\nHere is the R-squared value:')
    print(r2_score(actuals, predictions))

    # 5. pos and neg differences
    calculate_and_print_differences(predictions, actuals)
    # 6.

    actuals_preds = zip(actuals, predictions)
    # Sort by PREDICTED value, since this is what what we will know at the time we make a prediction
    actuals_preds.sort(key=lambda pair: pair[1])
    actuals_sorted = [act for act, pred in actuals_preds]
    predictions_sorted = [pred for act, pred in actuals_preds]

    print('Here\'s how the trained predictor did on each successive decile (ten percent chunk) of the predictions:')
    for i in range(1,10):
        print('\n**************')
        print('Bucket number:')
        print(i)
        # There's probably some fenceposting error here
        min_idx = int((i - 1) / 10.0 * len(actuals_sorted))
        max_idx = int(i / 10.0 * len(actuals_sorted))
        actuals_for_this_decile = actuals_sorted[min_idx:max_idx]
        predictions_for_this_decile = predictions_sorted[min_idx:max_idx]

        print('Avg predicted val in this bucket')
        print(sum(predictions_for_this_decile) * 1.0 / len(predictions_for_this_decile))
        print('Avg actual val in this bucket')
        print(sum(actuals_for_this_decile) * 1.0 / len(actuals_for_this_decile))
        print('RMSE for this bucket')
        print(mean_squared_error(actuals_for_this_decile, predictions_for_this_decile)**0.5)
        calculate_and_print_differences(predictions_for_this_decile, actuals_for_this_decile)

    print('')
    print('\n***********************************************\n\n')


def write_gs_param_results_to_file(trained_gs, most_recent_filename):

    timestamp_time = datetime.datetime.now()
    write_most_recent_gs_result_to_file(trained_gs, most_recent_filename, timestamp_time)

    grid_scores = trained_gs.grid_scores_
    scorer = trained_gs.scorer_
    best_score = trained_gs.best_score_

    file_name = 'pipeline_grid_search_results.csv'
    write_header = False
    if not os.path.isfile(file_name):
        write_header = True

    with open(file_name, 'a') as results_file:
        writer = csv.writer(results_file, dialect='excel')
        if write_header:
            writer.writerow(['timestamp', 'scorer', 'best_score', 'all_grid_scores'])
        writer.writerow([timestamp_time, scorer, best_score, grid_scores])


def write_most_recent_gs_result_to_file(trained_gs, most_recent_filename, timestamp):

    timestamp_time = timestamp
    grid_scores = trained_gs.grid_scores_
    scorer = trained_gs.scorer_
    best_score = trained_gs.best_score_

    file_name = most_recent_filename

    write_header = False
    make_header = False
    if not os.path.isfile(most_recent_filename):
        header_row = ['timestamp', 'scorer', 'best_score', 'cv_mean', 'cv_all']
        write_header = True
        make_header = True

    rows_to_write = []

    for score in grid_scores:

        row = [timestamp_time, scorer, best_score, score[1], score[2]]

        for k, v in score[0].items():
            if make_header:
                header_row.append(k)
            row.append(v)
        rows_to_write.append(row)
        make_header = False


    with open(file_name, 'a') as results_file:
        writer = csv.writer(results_file, dialect='excel')
        if write_header:
            writer.writerow(header_row)
        for row in rows_to_write:
            writer.writerow(row)


def get_feature_selection_model_from_name(type_of_estimator, model_name):
    # TODO(PRESTON): eventually let threshold be user-configurable (or grid_searchable)
    # TODO(PRESTON): optimize the params used here
    model_map = {
        'classifier': {
            'SelectFromModel': SelectFromModel(RandomForestClassifier(n_jobs=-1)),
            'RFECV': RFECV(estimator=RandomForestClassifier(n_jobs=-1), step=0.1),
            'GenericUnivariateSelect': GenericUnivariateSelect(),
            'RandomizedSparse': RandomizedLogisticRegression(),
            'KeepAll': 'KeepAll'
        },
        'regressor': {
            'SelectFromModel': SelectFromModel(RandomForestRegressor(n_jobs=-1, max_depth=10, n_estimators=15), threshold='0.5*mean'),
            'RFECV': RFECV(estimator=RandomForestRegressor(n_jobs=-1), step=0.1),
            'GenericUnivariateSelect': GenericUnivariateSelect(),
            'RandomizedSparse': RandomizedLasso(),
            'KeepAll': 'KeepAll'
        }
    }

    return model_map[type_of_estimator][model_name]


class FeatureSelectionTransformer(BaseEstimator, TransformerMixin):


    def __init__(self, type_of_estimator, column_descriptions, feature_selection_model='SelectFromModel'):

        self.column_descriptions = column_descriptions
        self.type_of_estimator = type_of_estimator
        self.feature_selection_model = feature_selection_model


    def fit(self, X, y=None):

        self.selector = get_feature_selection_model_from_name(self.type_of_estimator, self.feature_selection_model)

        if self.selector == 'KeepAll':
            if scipy.sparse.issparse(X):
                num_cols = X.shape[0]
            else:
                num_cols = len(X[0])

            self.support_mask = [True for col_idx in range(num_cols) ]
        else:
            self.selector.fit(X, y)
            self.support_mask = self.selector.get_support()

        end_time = datetime.datetime.now()

        return self


    def transform(self, X, y=None):

        if self.selector == 'KeepAll':
            return X
        else:
            transformed_X = self.selector.transform(X)
            return transformed_X


def rmse_scoring(estimator, X, y, took_log_of_y=False, advanced_scoring=False):
    if isinstance(estimator, GradientBoostingRegressor):
        X = X.toarray()
    predictions = estimator.predict(X)
    if took_log_of_y:
        for idx, val in enumerate(predictions):
            predictions[idx] = math.exp(val)
    rmse = mean_squared_error(y, predictions)**0.5
    if advanced_scoring == True:
        advanced_scoring_regressors(predictions, y)
    return - 1 * rmse


def brier_score_loss_wrapper(estimator, X, y, advanced_scoring=False):
    if isinstance(estimator, GradientBoostingClassifier):
        X = X.toarray()
    clean_ys = []
    # try:
    for val in y:
        val = int(val)
        clean_ys.append(val)
    y = clean_ys
    # except:
    #     pass
    predictions = estimator.predict_proba(X)
    probas = [row[1] for row in predictions]
    score = brier_score_loss(y, probas)
    if advanced_scoring:
        return (-1 * score, probas)
    else:
        return -1 * score


# Used in CustomSparseScaler
def calculate_scaling_ranges(X, col, min_percentile=0.05, max_percentile=0.95):

    series_vals = X[col]
    good_vals_indexes = series_vals.notnull()

    series_vals = list(series_vals[good_vals_indexes])
    series_vals = sorted(series_vals)

    max_val_idx = int(max_percentile * len(series_vals)) - 1
    min_val_idx = int(min_percentile * len(series_vals))

    if len(series_vals) > 0:
        max_val = series_vals[max_val_idx]
        min_val = series_vals[min_val_idx]
    else:
        # print('This column appears to have only nan values, and will be ignored:')
        # print(col)
        return 'ignore'

    inner_range = max_val - min_val

    if inner_range == 0:
        # Used to do recursion here, which is prettier and uses less code, but since we've already got the filtered and sorted series_vals, it makes sense to use those to avoid duplicate computation
        # Grab the absolute largest max and min vals, and see if there is any difference in them, since our 95th and 5th percentile vals had no difference between them
        max_val = series_vals[len(series_vals) - 1]
        min_val = series_vals[0]
        inner_range = max_val - min_val

        if inner_range == 0:
            # If this is a binary field, keep all the values in it, just make sure they're scaled to 1 or 0.
            if max_val == 1:
                min_val = 0
                inner_range = 1
            else:
                # If this is just a column that holds all the same values for everything though, delete the column to save some space
                # print('This column appears to have 0 variance (the max and min values are the same), and will be ignored:')
                # print(col)
                return 'ignore'

    col_summary = {
        'max_val': max_val
        , 'min_val': min_val
        , 'inner_range': inner_range
    }

    return col_summary

# Scale sparse data to the 95th and 5th percentile
# Only do so for values that actuall exist (do absolutely nothing with rows that do not have this data point)
class CustomSparseScaler(BaseEstimator, TransformerMixin):


    def __init__(self, column_descriptions, truncate_large_values=False, perform_feature_scaling=True):
        self.column_descriptions = column_descriptions

        self.numeric_col_descs = set([None, 'continuous', 'numerical', 'numeric', 'float', 'int'])
        # Everything in column_descriptions (except numeric_col_descs) is a non-numeric column, and thus, cannot be scaled
        self.cols_to_avoid = set([k for k, v in column_descriptions.items() if v not in self.numeric_col_descs])

        # Setting these here so that they can be grid searchable
        # Truncating large values is an interesting strategy. It forces all values to fit inside the 5th - 95th percentiles.
        # Essentially, it turns any really large (or small) values into reasonably large (or small) values.
        self.truncate_large_values = truncate_large_values
        self.perform_feature_scaling = perform_feature_scaling


    def fit(self, X, y=None):
        self.column_ranges = {}
        self.cols_to_ignore = []

        if self.perform_feature_scaling:

            for col in X.columns:
                if col not in self.cols_to_avoid:
                    col_summary = calculate_scaling_ranges(X, col, min_percentile=0.05, max_percentile=0.95)
                    if col_summary == 'ignore':
                        self.cols_to_ignore.append(col)
                    else:
                        self.column_ranges[col] = col_summary

        return self


    # Perform basic min/max scaling, with the minor caveat that our min and max values are the 10th and 90th percentile values, to avoid outliers.
    def transform(self, X, y=None):

        if isinstance(X, dict):
            for col, col_dict in self.column_ranges.items():
                if col in X:
                    X[col] = scale_val(val=X[col], min_val=col_dict['min_val'], total_range=col_dict['inner_range'], truncate_large_values=self.truncate_large_values)
        else:

            if len(self.cols_to_ignore) > 0:
                X = safely_drop_columns(X, self.cols_to_ignore)
                # X = X.drop(self.cols_to_ignore, axis=1)

            for col, col_dict in self.column_ranges.items():
                if col in X.columns:
                    min_val = col_dict['min_val']
                    inner_range = col_dict['inner_range']
                    X[col] = X[col].apply(lambda x: scale_val(x, min_val, inner_range, self.truncate_large_values))

        return X


def scale_val(val, min_val, total_range, truncate_large_values=False):
    scaled_value = (val - min_val) / total_range
    if truncate_large_values:
        if scaled_value < 0:
            scaled_value = 0
        elif scaled_value > 1:
            scaled_value = 1

    return scaled_value


def safely_drop_columns(df, cols_to_drop):
    safe_cols_to_drop = []
    for col in cols_to_drop:
        if col in df.columns:
            safe_cols_to_drop.append(col)

    df = df.drop(safe_cols_to_drop, axis=1)
    return df
