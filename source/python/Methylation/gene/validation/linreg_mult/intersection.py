import pathlib
from Infrastructure.file_system import *
import os.path
import math
import numpy as np
import pandas as pd
import scipy.stats as stats
import operator
from dicts import *
import statsmodels.api as sm
from sklearn.linear_model import ElasticNetCV, ElasticNet
from config import *
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics
from Infrastructure.load import *
from Infrastructure.save import *
from linreg_mult.routines import *
from method import *

train_size = 482
test_size = 174
num_top_genes = 100
num_bootstrap_runs = 500

method = Method.enet
val_method = Validation.linreg_mult
gd_type_order = GeneDataType.mean_der_normed
gd_type_vals = GeneDataType.mean
geo_type = GeoType.any
host_name = socket.gethostname()
fs_type = FSType.local_big
if host_name == 'MSI':
    fs_type = FSType.local_msi
elif host_name == 'DESKTOP-K9VO2TI':
    fs_type = FSType.local_big
db_type = DataBaseType.GSE40279
config = Config(fs_type, db_type, geo_type)
if db_type is DataBaseType.GSE40279:
    config = ConfigGSE40279(fs_type, db_type, geo_type)
elif db_type is DataBaseType.GSE52588:
    config = ConfigGSE52588(fs_type, db_type, geo_type)

attributes = get_attributes(config)

gene_names = get_top_gene_names(config, gd_type_order, method, num_top_genes)
gene_vals = get_top_gene_vals(config, gd_type_vals, gene_names)

counts, R2s = R2_from_count(gene_vals, attributes)

fn = 'gene/' + val_method.value + '/' + method.value + '_R2s_order(' + gd_type_order.value + ')_vals(' + gd_type_vals.value + ')' +  geo_type.value + '.txt'
fn = get_result_path(fs_type, db_type, fn)
save_R2(fn, counts, R2s)

metrics_names, metrics_vals = validation_metrics(gene_vals, attributes, test_size, train_size, num_bootstrap_runs)

fn = 'gene/' + val_method.value + '/' + method.value +'_metrics_order(' + gd_type_order.value + ')_vals(' + gd_type_vals.value + ')' +  geo_type.value + '.txt'
fn = get_result_path(fs_type, db_type, fn)
save_params(fn, metrics_names, metrics_vals)

print(linreg_mult_with_const(attributes, gene_vals).summary())

