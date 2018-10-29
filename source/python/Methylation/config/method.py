from enum import Enum
import math


class Method(Enum):
    enet = 'enet'
    linreg = 'linreg'
    linreg_with_rejection = 'linreg_with_rejection'
    linreg_bend = 'linreg_bend'
    linreg_dispersion = 'linreg_dispersion'
    linreg_variance = 'linreg_variance'
    linreg_ols = 'linreg_ols'
    anova = 'anova'
    spearman = 'spearman'
    manova = 'manova'
    random_forest = 'random_forest'
    k_means = 'k_means'
    mean_shift = 'mean_shift'
    linreg_mult = 'linreg_mult'
    match = 'match'
    gender_specific = 'gender_specific'
    moment = 'moment'

def get_top_fn(method, params_dict):
    fn = 'top.txt'
    if method is Method.linreg_bend:
        fn = 'top'
        for key in params_dict:
            fn += '_' + key + '(' + str(format(params_dict[key], '0.4e')) + ')'
        fn += '.txt'
    elif method is Method.linreg_dispersion:
        fn = 'top'
        for key in params_dict:
            fn += '_' + key + '(' + str(format(params_dict[key], '0.4e')) + ')'
        fn += '.txt'
    return fn

def get_method_metrics(method, is_clustering=False):
    metrics = []
    clustering_metrics = [
        'cluster_mean_shift',
        'cluster_affinity_prop'
    ]
    if method is Method.linreg:
        metrics = [
            'r_value',
            'p_values',
            'slope',
            'intercept'
        ]
        if is_clustering:
            metrics = metrics + clustering_metrics
    elif method is Method.linreg_with_rejection:
        metrics = [
            'r_value',
            'p_values',
            'slope',
            'intercept'
        ]
        if is_clustering:
            metrics = metrics + clustering_metrics
    elif method is Method.linreg_with_rejection:
        metrics = [
            'r_value',
            'p_values',
            'slope',
            'intercept'
        ]
        if is_clustering:
            metrics = metrics + clustering_metrics
    elif method is Method.linreg_bend:
        metrics = [
            'angles',
            'slope_left',
            'intercept_left',
            'r_value_left',
            'p_value_left',
            'std_err_left',
            'slope_right',
            'intercept_right',
            'r_value_right',
            'p_value_right',
            'std_err_right'
        ]
    elif method is Method.linreg_dispersion:
        metrics = [
            'slope_left',
            'intercept_left',
            'r_value_left',
            'p_value_left',
            'std_err_left',
            'slope_right',
            'intercept_right',
            'r_value_right',
            'p_value_right',
            'std_err_right'
        ]
    elif method is Method.linreg_variance:
        metrics = [
            'r_value',
            'p_values',
            'slope',
            'intercept',
            'r_value_diff',
            'p_values_diff',
            'slope_diff',
            'intercept_diff'
        ]
        if is_clustering:
            metrics = metrics + clustering_metrics
    elif method is Method.manova:
        metrics = ['pval']

    return metrics

def get_method_order_metrics(method):
    metrics = []
    if method is Method.linreg_ols:
        metrics = [
            'names',
            'areas',
            'areas_normed'
        ]
    elif method is Method.manova:
        metrics = ['names']

    return metrics

def get_method_main_metric(method):
    metric = ''
    if method is Method.linreg:
        metric = 'r_value'
    elif method is Method.manova:
        metric = 'pval'
    return metric

def metric_processing(method, metric):
    if method is Method.linreg:
        return float(metric)
    elif method is Method.manova:
        return -math.log10(float(metric))
    else:
        return float(metric)
