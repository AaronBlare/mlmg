from config.config import *
from annotations.bop import *
from infrastructure.load.cpg_data import load_cpg_data
from statsmodels.multivariate.manova import MANOVA
from statsmodels.stats.multitest import multipletests
from infrastructure.save.features import save_features
from sklearn.cluster import MeanShift, estimate_bandwidth, AffinityPropagation
from method.clustering.order import *
import pandas as pd


def save_top_manova(config, attributes_types, attribute_target, window=3, test=MANOVATest.pillai_bartlett, is_clustering=False):
    dict_bop_cpgs = get_dict_bop_cpgs(config)
    dict_bop_genes = get_dict_bop_genes(config, dict_bop_cpgs)
    cpgs, betas = load_cpg_data(config)

    atr_table = []
    atr_cols = []
    for atr_type in attributes_types:
        if isinstance(atr_type, Attribute):
            atr_table.append(get_attributes(config, atr_type))
        elif isinstance(atr_type, CellPop):
            atr_table.append(get_cell_pop(config, [atr_type]))
        atr_cols.append(atr_type.value)

    num_bops = 0
    bops_passed = []
    p_values = []
    for bop in dict_bop_cpgs:
        curr_cpgs = dict_bop_cpgs.get(bop)
        cpgs_passed = []
        for cpg in curr_cpgs:
            if cpg in cpgs:
                cpgs_passed.append(cpg)
        if len(cpgs_passed) > 2:
            pvals_on_bop = []
            for win_id in range(0, len(cpgs_passed) - 2):
                val_table = []
                val_cols = []
                for cpg_id in range(0, window):
                    cpg = cpgs_passed[win_id + cpg_id]
                    beta = betas[cpgs.index(cpg)]
                    val_table.append(beta)
                    val_cols.append('cpg_'+str(cpg_id))
                table = atr_table + val_table
                cols = atr_cols + val_cols

                formula = val_cols[0]
                for val_col_id in range(1, len(val_cols)):
                    val_col = val_cols[val_col_id]
                    formula += ' + ' + val_col
                formula += ' ~ ' + atr_cols[0]
                for atr_col_id in range(1, len(atr_cols)):
                    atr_col = atr_cols[atr_col_id]
                    formula += ' + ' + atr_col

                table = list(map(list, zip(*table)))
                x = pd.DataFrame(table, columns=cols)
                manova = MANOVA.from_formula(formula, x)
                mv_test_res = manova.mv_test()
                pvals = mv_test_res.results[attribute_target.value]['stat'].values[0:4, 4]
                target_pval = pvals[0]
                if test is MANOVATest.wilks:
                    target_pval = pvals[0]
                elif test is MANOVATest.pillai_bartlett:
                    target_pval = pvals[1]
                elif test is MANOVATest.lawley_hotelling:
                    target_pval = pvals[2]
                elif test is MANOVATest.roy:
                    target_pval = pvals[3]
                pvals_on_bop.append(target_pval)
            min_pval = np.min(pvals_on_bop)
            bops_passed.append(bop)
            p_values.append(min_pval)
        num_bops += 1
        if num_bops % config.print_rate == 0:
            print('num_bops: ' + str(num_bops))

    reject, p_values_corrected, alphacSidak, alphacBonf = multipletests(p_values, 0.05, method='fdr_bh')
    order = np.argsort(p_values_corrected)
    bops_sorted = list(np.array(bops_passed)[order])
    p_values_sorted = list(np.array(p_values_corrected)[order])

    clusters_mean_shift = []
    clusters_affinity_prop = []
    if is_clustering:
        metrics_sorted_np = np.asarray(list(map(np.log10, p_values_sorted))).reshape(-1, 1)
        bandwidth = estimate_bandwidth(metrics_sorted_np)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(metrics_sorted_np)
        labels_mean_shift = list(ms.labels_)
        clusters_mean_shift = clustering_order(labels_mean_shift)
        af = AffinityPropagation().fit(metrics_sorted_np)
        labels_affinity_propagation = list(af.labels_)
        clusters_affinity_prop = clustering_order(labels_affinity_propagation)
        features = [
            bops_sorted,
            clusters_mean_shift,
            clusters_affinity_prop,
            p_values_sorted
        ]
        fn = 'top_with_clustering.txt'
    else:
        features = [
            bops_sorted,
            p_values_sorted
        ]
        fn = 'top.txt'
    fn = get_result_path(config, fn)
    save_features(fn, features)

    genes_sorted = []
    p_values_genes = []
    clusters_mean_shift_genes = []
    clusters_affinity_prop_genes = []
    for id in range(0, len(bops_sorted)):
        bop = bops_sorted[id]
        p_value = p_values_sorted[id]
        if is_clustering:
            cluster_mean_shift = clusters_mean_shift[id]
            cluster_affinity_prop = clusters_affinity_prop[id]
        else:
            cluster_mean_shift = []
            cluster_affinity_prop = []
        if bop in dict_bop_genes:
            genes = dict_bop_genes.get(bop)
            for gene in genes:
                if gene not in genes_sorted:
                    genes_sorted.append(gene)
                    p_values_genes.append(p_value)
                    if is_clustering:
                        clusters_mean_shift_genes.append(cluster_mean_shift)
                        clusters_affinity_prop_genes.append(cluster_affinity_prop)

    config.data_type = DataType.gene
    gene_data_type = config.gene_data_type
    geo_type = config.geo_type
    config.gene_data_type = GeneDataType.from_bop
    config.geo_type = GeoType.from_bop

    if is_clustering:
        fn = 'top_with_clustering.txt'
        features = [
            genes_sorted,
            clusters_mean_shift_genes,
            clusters_affinity_prop_genes,
            p_values_genes
        ]
    else:
        fn = 'top.txt'
        features = [
            genes_sorted,
            p_values_genes,
        ]
    fn = get_result_path(config, fn)
    save_features(fn, features)

    config.gene_data_type = gene_data_type
    config.geo_type = geo_type
    config.data_type = DataType.bop
