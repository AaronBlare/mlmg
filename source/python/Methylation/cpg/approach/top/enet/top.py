import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import ShuffleSplit
from infrastructure.load.attributes import get_main_attributes
from infrastructure.load.cpg_data import load_cpg_data
from infrastructure.load.params import load_params_dict
from infrastructure.file_system import get_result_path
from infrastructure.save.features import save_features
from annotation.regular import get_dict_cpg_gene
from config.types import *


def save_top_enet(config, num_bootstrap_runs=100, num_top=100):

    dict_cpg_gene = get_dict_cpg_gene(config)
    params_dict = load_params_dict(config)
    alpha = params_dict.get('alpha')
    l1_ratio = params_dict.get('l1_ratio')

    attributes = get_main_attributes(config)
    cpgs_passed, vals_passed = load_cpg_data(config)

    rs = ShuffleSplit(num_bootstrap_runs, config.test_size, config.train_size)
    indexes = np.linspace(0, len(attributes) - 1, len(attributes), dtype=int).tolist()
    enet_X = np.array(vals_passed).T.tolist()

    bootstrap_id = 0
    cpg_top_dict = {}
    for train_index, test_index in rs.split(indexes):
        print('bootstrap_id: ' + str(bootstrap_id))

        enet = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)

        enet_X_train = list(np.array(enet_X)[train_index])
        enet_X_test = list(np.array(enet_X)[test_index])
        enet_y_train = list(np.array(attributes)[train_index])
        enet_y_test = list(np.array(attributes)[test_index])

        enet = enet.fit(enet_X_train, enet_y_train)
        coef = enet.coef_

        order = np.argsort(list(map(abs, coef)))[::-1]
        coef_sorted = list(np.array(coef)[order])
        cpg_sorted = list(np.array(cpgs_passed)[order])
        coef_top = coef_sorted[0:num_top]
        cpg_top = cpg_sorted[0:num_top]
        gene_sorted = []
        for id in range(0, len(cpg_sorted)):
            cpg = cpg_sorted[id]
            genes = dict_cpg_gene.get(cpg)
            for gene in genes:
                if gene not in gene_sorted:
                    gene_sorted.append(gene)
        gene_top = gene_sorted[0:num_top]

        for top_id in range(0, num_top):
            cpg = cpg_top[top_id]
            if cpg in cpg_top_dict:
                cpg_top_dict[cpg] += 1
            else:
                cpg_top_dict[cpg] = 1

        bootstrap_id += 1

    cpgs = list(cpg_top_dict.keys())
    counts = list(cpg_top_dict.values())
    order = np.argsort(list(map(abs, counts)))[::-1]
    cpgs_sorted = list(np.array(cpgs)[order])
    counts_sorted = list(np.array(counts)[order])
    genes_sorted = []
    counts_genes = []
    for id in range(0, len(cpgs_sorted)):
        cpg = cpgs_sorted[id]
        count = counts_sorted[id]
        genes = dict_cpg_gene.get(cpg)
        for gene in genes:
            if gene not in genes_sorted:
                genes_sorted.append(gene)
                counts_genes.append(count)

    fn = 'top.txt'
    fn = get_result_path(config, fn)
    save_features(fn, [cpgs_sorted, counts_sorted])

    config.approach_gd = GeneDataType.from_cpg
    config.dt = DataType.gene
    fn = 'top.txt'
    fn = get_result_path(config, fn)
    save_features(fn, [genes_sorted, counts_genes])
    config.dt = DataType.cpg
