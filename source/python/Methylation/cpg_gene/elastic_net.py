import pathlib
from Infrastructure.file_system import *
import os.path
import math
import numpy as np
import pandas as pd
import scipy.stats as stats
from dicts import *
import statsmodels.api as sm
from sklearn.linear_model import ElasticNet

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

print_rate = 10000

num_top_opt = 100

fs_type = FSType.local_big
db_type = DataBaseType.GSE40279
geo_type = GeoType.islands_shores

dict_cpg_gene, dict_cpg_map = get_dicts(fs_type, db_type, geo_type)

fn = 'attribute.txt'
ages = []
full_path = get_full_path(fs_type, db_type, fn)
with open(full_path) as f:
    for line in f:
        ages.append(int(line))

fn = db_type.value + '_average_beta.txt'
full_path = get_full_path(fs_type, db_type, fn)

num_lines = 0

cpgs = []
rhos = []
pvals = []
vals_passed = []

f = open(full_path)
first_line = f.readline()
col_names = first_line.split('\t')

for line in f:

    col_vals = line.split('\t')
    CpG = col_vals[0]
    vals = list(map(float, col_vals[1::]))

    if CpG in dict_cpg_gene:

        slope, intercept, r_value, p_value, std_err = stats.linregress(vals, ages)

        genes = dict_cpg_gene.get(CpG)

        if genes is not None:

            cpgs.append(CpG)
            rhos.append(r_value)
            vals_passed.append(vals)

    num_lines += 1
    if num_lines % print_rate == 0:
        print('num_lines: ' + str(num_lines))

order = np.argsort(list(map(abs, rhos)))[::-1]
rhos_opt = list(np.array(rhos)[order])
cpgs_opt = list(np.array(cpgs)[order])
vals_passed_opt = list(np.array(vals_passed)[order])

genes_spec = []
cpg_spec = []
vals_spec = []
rhos_spec = []

for id in range(0, len(cpgs_opt)):
    cpg = cpgs_opt[id]
    rho = rhos_opt[id]
    vals = vals_passed_opt[id]
    genes = dict_cpg_gene.get(cpg)
    for gene in genes:
        if gene not in genes_spec:
            genes_spec.append(gene)
            cpg_spec.append(cpg)
            vals_spec.append(vals)
            rhos_spec.append(rho)

regr = ElasticNet()
elastic_net_X = list(map(list, zip(*vals_spec)))
regr.fit(elastic_net_X, ages)
coef = regr.coef_

order = np.argsort(list(map(abs, coef)))[::-1]
genes = list(np.array(genes_spec)[order])
vals = list(np.array(vals_spec)[order])

top_R = []
top_coeff = []
top_num = []

for num_opt in range(0, num_top_opt):
    reg_res = reg_m(ages, vals[0:num_opt + 1])
    top_num.append(num_opt + 1)
    top_coeff.append(reg_res.rsquared)
    top_R.append(reg_res.params[0])

info = np.zeros(len(top_num), dtype=[('var1', int), ('var2', float), ('var3', float)])
fmt = "%d %0.18e %0.18e"
info['var1'] = top_num
info['var2'] = top_coeff
info['var3'] = top_R
np.savetxt('elastic.txt', info, fmt=fmt)
