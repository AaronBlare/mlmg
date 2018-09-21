from method.enet.routines import *
from infrastructure.load.attributes import get_attributes
from infrastructure.load.gene_data import load_gene_data
from infrastructure.path import get_result_path
from infrastructure.save.features import save_features
from sklearn.cluster import MeanShift, estimate_bandwidth, AffinityPropagation
from method.clustering.order import *
from scipy import stats


def save_top_linreg_modified(config):
    attributes = get_attributes(config)
    genes, vals = load_gene_data(config)

    p_values = []
    r_values = []
    slopes = []
    intercepts = []
    for id in range(0, len(genes)):
        val = vals[id]
        slope, intercept, r_value, p_value, std_err = stats.linregress(attributes, val)
        r_values.append(r_value)
        p_values.append(p_value)
        slopes.append(slope)
        intercepts.append(intercept)

    order_mean = np.argsort(list(map(abs, r_values)))[::-1]
    p_values_sorted = list(np.array(p_values)[order_mean])
    r_values_sorted = list(np.array(r_values)[order_mean])
    slopes_sorted = list(np.array(slopes)[order_mean])
    intercepts_sorted = list(np.array(intercepts)[order_mean])
    genes_sorted = list(np.array(genes)[order_mean])

    metrics_sorted_np = np.asarray(list(map(abs, r_values_sorted))).reshape(-1, 1)
    bandwidth = estimate_bandwidth(metrics_sorted_np)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(metrics_sorted_np)
    labels_mean_shift = list(ms.labels_)
    clusters_mean_shift = clustering_order(labels_mean_shift)
    af = AffinityPropagation().fit(metrics_sorted_np)
    labels_affinity_propagation = list(af.labels_)
    clusters_affinity_prop = clustering_order(labels_affinity_propagation)

    fn = get_result_path(config, 'top.txt')
    save_features(fn, [genes_sorted, clusters_mean_shift, clusters_affinity_prop, r_values_sorted, p_values_sorted, slopes_sorted, intercepts_sorted])
