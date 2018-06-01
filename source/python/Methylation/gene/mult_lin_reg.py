import pathlib
from Infrastructure.file_system import *
import os.path
import math
import numpy as np
import pandas as pd
import scipy.stats as stats
from dicts import get_dicts
from gen_files.geo import *
import statsmodels.api as sm

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

fs_type = FSType.local_big
db_type = DataBaseType.GSE40279
geo_type = GeoType.islands_shores

num_top = 100
num_top_opt = 5

fn = 'table.txt'
full_path = get_full_path(fs_type, db_type, fn)
file = open(full_path)
table = file.read().splitlines()

fn = 'attribute.txt'
ages = []
full_path = get_full_path(fs_type, db_type, fn)
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

fn = 'gene_mean' + geo_type.value + '.txt'
full_path = get_full_path(fs_type, db_type, fn)
f = open(full_path)
for line in f:
    col_vals = line.split(' ')
    gene = col_vals[0]
    vals = list(map(float, col_vals[1::]))
    mean_names.append(gene)
    mean.append(vals)

fn = 'gene_std' + geo_type.value + '.txt'
full_path = get_full_path(fs_type, db_type, fn)
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

order_mean = np.argsort(mean_p_values)
genes_opt_mean = list(np.array(mean_names)[order_mean])
mean_opt_mean = list(np.array(mean)[order_mean])

print(reg_m(ages, mean_opt_mean[0:num_top_opt]).summary(xname=genes_opt_mean[0:num_top_opt], yname='age'))

genes_match = []
mean_match = []
for gene_id in range(0, num_top):
    curr_gene = genes_opt_mean[gene_id]
    curr_mean = mean_opt_mean[gene_id]
    if curr_gene in table:
        genes_match.append(curr_gene)
        mean_match.append(curr_mean)

print('Claudio match')
print(reg_m(ages, mean_match[0:num_top_opt]).summary(xname=genes_match[0:num_top_opt], yname='age'))
