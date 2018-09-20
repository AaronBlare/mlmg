from infrastructure.path import *
from infrastructure.load.routines import line_proc
from infrastructure.path import get_result_path
import numpy as np


def load_top_gene_names_by_article(config, fn):
    full_path = get_origin_path(config, fn)
    file = open(full_path)
    table = file.read().splitlines()
    return table

def load_top_gene_data(config, num_top):
    gene_names = load_top_gene_names(config, num_top)
    gene_vals = load_top_gene_vals(config, gene_names)
    return gene_names, gene_vals

def load_top_gene_names(config, num_top):
    fn = 'top.txt'
    fn = get_result_path(config, fn)
    f = open(fn)
    gene_names = []
    for line in f:
        gene = line.split(' ')[0].rstrip()
        gene_names.append(gene)
    gene_names = gene_names[0:num_top]
    return gene_names

def load_top_gene_linreg_dict(config, num_top):
    fn = 'top.txt'
    fn = get_result_path(config, fn)
    f = open(fn)
    names = []
    metrics = []
    slopes = []
    clusters = []
    for line in f:
        cols = line.split(' ')
        gene = cols[0].rstrip()
        slope = float(cols[5].rstrip())
        metric = float(cols[3].rstrip())
        cluster = int(cols[1].rstrip())
        names.append(gene)
        slopes.append(slope)
        metrics.append(metric)
        clusters.append(cluster)
    names = names[0:num_top]
    slopes = slopes[0:num_top]
    metrics = metrics[0:num_top]
    clusters = clusters[0:num_top]

    curr_cluster = clusters[0]
    mod_cluster = 0
    sorted_clusters = []
    for cl_id in range(0, len(clusters)):
        if clusters[cl_id] != curr_cluster:
            curr_cluster = clusters[cl_id]
            mod_cluster += 1
        sorted_clusters.append(mod_cluster)

    top_dict = {}
    for id in range(0, len(names)):
        top_dict[names[id]] = [id, metrics[id], sorted_clusters[id], slopes[id]]

    return top_dict

def load_top_gene_vals(config, genes_top):
    indexes = config.indexes
    dict_top = {}
    fn = 'gene_data.txt'
    fn = get_gene_data_path(config, fn)
    f = open(fn)
    for line in f:
        col_vals = line.split(' ')
        gene = col_vals[0]
        vals = list(map(float, col_vals[1::]))
        vals = list(np.array(vals)[indexes])
        if gene in genes_top:
            dict_top[gene] = vals
    gene_vals = []
    for gene in genes_top:
        vals = dict_top.get(gene)
        gene_vals.append(vals)
    return gene_vals

def load_top_gene_names_by_cpg(config, method, num_top):
    fn = 'genes_from_cpg.txt'
    fn = get_result_path(config, fn)
    f = open(fn)
    gene_names = []
    for line in f:
        gene = line.split(' ')[0].rstrip()
        gene_names.append(gene)
    gene_names = gene_names[0:num_top]
    return gene_names

def load_top_cpg_data(config, method, num_top):
    indexes = config.indexes
    db_type = config.db_type
    print_rate = config.print_rate
    cpgs_top = []
    fn = 'top.txt'
    fn = get_result_path(config, fn)
    f = open(fn)
    for line in f:
        cpg = line.split(' ')[0].rstrip()
        cpgs_top.append(cpg)

    cpgs_top = cpgs_top[0:num_top]

    fn = db_type.value + '_average_beta.txt'
    path = get_path(config, fn)
    f = open(path)
    for skip_id in range(0, config.num_skip_lines):
        skip_line = f.readline()

    num_lines = 0
    dict_top = {}

    for line in f:

        col_vals = line_proc(config, line)
        cpg = col_vals[0]
        vals = list(map(float, col_vals[1::]))
        vals = list(np.array(vals)[indexes])

        if cpg in cpgs_top:
            dict_top[cpg] = vals

        num_lines += 1
        if num_lines % print_rate == 0:
            print('num_lines: ' + str(num_lines))

    vals_top = []
    for cpg in cpgs_top:
        vals = dict_top.get(cpg)
        vals_top.append(vals)

    return cpgs_top, vals_top

