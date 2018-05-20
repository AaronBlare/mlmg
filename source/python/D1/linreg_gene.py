import pathlib
from Infrastructure.file_system import *
import os.path
import math
import numpy as np
import pandas as pd
import scipy.stats as stats
from dicts import get_dict_cpg_gene

type = FSType.local_big
pval_lim = 1.0e-10
print_rate = 1000
num_top = 100

suffix = ''

fn = 'table.txt'
full_path = get_full_path(type, fn)
file = open(full_path)
table = file.read().splitlines()

fn = 'ages.txt'
ages = []
full_path = get_full_path(type, fn)
with open(full_path) as f:
    for line in f:
        ages.append(int(line))

num_genes = 0

mean_names = []
mean = []
mean_p_values = []
mean_slopes = []
mean_intercepts = []

std_names = []
std = []
std_p_values = []
std_slopes = []
std_intercepts = []

fn = 'gene_mean' + suffix + '.txt'
full_path = get_full_path(type, fn)
f = open(full_path)
for line in f:
    col_vals = line.split(' ')
    gene = col_vals[0]
    vals = list(map(float, col_vals[1::]))
    mean_names.append(gene)
    mean.append(vals)

fn = 'gene_std' + suffix + '.txt'
full_path = get_full_path(type, fn)
f = open(full_path)
for line in f:
    col_vals = line.split(' ')
    gene = col_vals[0]
    vals = list(map(float, col_vals[1::]))
    std_names.append(gene)
    std.append(vals)

for id in range(0, len(mean_names)):

    means = mean[id]
    stds = std[id]

    gene_name_mean = mean_names[id]
    gene_name_std = std_names[id]

    if gene_name_mean != gene_name_std:
        print('error')

    slope, intercept, r_value, p_value, std_err = stats.linregress(means, ages)
    mean_p_values.append(p_value)
    mean_slopes.append(slope)
    mean_intercepts.append(intercept)

    slope, intercept, r_value, p_value, std_err = stats.linregress(stds, ages)
    std_p_values.append(p_value)
    std_slopes.append(slope)
    std_intercepts.append(intercept)

mean_order = np.argsort(mean_p_values)
mean_p_values_opt = list(np.array(mean_p_values)[mean_order])
mean_slopes_opt = list(np.array(mean_slopes)[mean_order])
mean_intercepts_opt = list(np.array(mean_intercepts)[mean_order])
mean_genes_opt = list(np.array(mean_names)[mean_order])
info = np.zeros(len(mean_names), dtype=[('var1', 'U50'), ('var2', float), ('var3', float), ('var4', float)])
fmt = "%s %0.18e %0.18e %0.18e"
info['var1'] = mean_genes_opt
info['var2'] = mean_p_values_opt
info['var3'] = mean_slopes_opt
info['var4'] = mean_intercepts_opt
np.savetxt('linreg_genes_mean.txt', info, fmt=fmt)

std_order = np.argsort(std_p_values)
std_p_values_opt = list(np.array(std_p_values)[std_order])
std_slopes_opt = list(np.array(std_slopes)[std_order])
std_intercepts_opt = list(np.array(std_intercepts)[std_order])
std_genes_opt = list(np.array(std_names)[std_order])
info = np.zeros(len(std_names), dtype=[('var1', 'U50'), ('var2', float), ('var3', float), ('var4', float)])
fmt = "%s %0.18e %0.18e %0.18e"
info['var1'] = std_genes_opt
info['var2'] = std_p_values_opt
info['var3'] = std_slopes_opt
info['var4'] = std_intercepts_opt
np.savetxt('linreg_genes_std.txt', info, fmt=fmt)

genes_match = []
for gene in mean_genes_opt[0:num_top]:
    if gene in table:
        genes_match.append(gene)
np.savetxt('linreg_match_mean.txt', genes_match, fmt="%s")
print('top: ' + str(len(genes_match)))


genes_match = []
for gene in std_genes_opt[0:num_top]:
    if gene in table:
        genes_match.append(gene)
np.savetxt('linreg_match_std.txt', genes_match, fmt="%s")
print('top: ' + str(len(genes_match)))