from annotations.regular import get_dict_cpg_gene
from infrastructure.path import get_path
from config.types import *
from infrastructure.load.routines import line_proc
import numpy as np


def get_non_inc_cpgs(config):
    cpg_non_inc = []
    if config.db is DataBaseType.GSE40279:
        cpg_non_inc = []
    elif config.db is DataBaseType.GSE52588:
        pval_lim = 0.05
        pval_part = 0.75

        cpgs, pvals = load_cpg_pval_data(config)
        cpg_non_inc = []
        for id in range(0, len(cpgs)):
            curr_cpg = cpgs[id]
            curr_pvals = pvals[id]

            num_big_pvals = 0
            for pval in curr_pvals:
                if pval > pval_lim:
                    num_big_pvals += 1

            if float(num_big_pvals) / float(len(curr_pvals)) > pval_part:
                cpg_non_inc.append(curr_cpg)
    return cpg_non_inc

def load_cpg_data(config):
    indexes = config.indexes
    dict_cpg_gene = get_dict_cpg_gene(config)

    fn = 'average_beta.txt'
    full_path = get_path(config, fn)
    f = open(full_path)
    for skip_id in range(0, config.num_skip_lines):
        skip_line = f.readline()

    num_lines = 0
    cpgs_passed = []
    vals_passed = []

    cpg_non_inc = get_non_inc_cpgs(config)

    for line in f:

        col_vals = line_proc(config, line)

        is_none = False
        if config.miss_tag in col_vals:
            is_none = True

        if not is_none:
            cpg = col_vals[0]
            vals = list(map(float, col_vals[1::]))
            vals = list(np.array(vals)[indexes])

            if cpg not in cpg_non_inc:
                if cpg in dict_cpg_gene:
                    vals_passed.append(vals)
                    cpgs_passed.append(cpg)

        num_lines += 1
        if num_lines % config.print_rate == 0:
            print('num_lines: ' + str(num_lines))

    f.close()

    return cpgs_passed, vals_passed

def load_cpg_data_raw(config):
    indexes = config.indexes
    dict_cpg_gene = get_dict_cpg_gene(config)

    fn = 'average_beta.txt'
    full_path = get_path(config, fn)
    f = open(full_path)
    for skip_id in range(0, config.num_skip_lines):
        skip_line = f.readline()

    num_lines = 0
    cpgs_passed = []
    vals_passed = []

    for line in f:
        col_vals = line_proc(config, line)
        cpg = col_vals[0]
        vals = col_vals[1::]
        vals = list(np.array(vals)[indexes])

        vals_passed.append(vals)
        cpgs_passed.append(cpg)

        num_lines += 1
        if num_lines % config.print_rate == 0:
            print('num_lines: ' + str(num_lines))

    f.close()

    return cpgs_passed, vals_passed

def load_cpg_pval_data(config):
    indexes = config.indexes

    fn = 'raw_data.txt'
    fn = get_path(config, fn)
    f = open(fn)
    for skip_id in range(0, config.num_skip_lines):
        skip_line = f.readline()

    num_lines = 0
    cpgs_passed = []
    vals_passed = []
    for line in f:
        col_vals = line.split('\t')
        cpg = col_vals[0].replace('"', '')
        vals = list(map(float, col_vals[1::]))
        pvals = vals[2::3]
        pvals = list(np.array(pvals)[indexes])

        cpgs_passed.append(cpg)
        vals_passed.append(pvals)

        num_lines += 1
        if num_lines % config.print_rate == 0:
            print('num_lines: ' + str(num_lines))

    f.close()

    return cpgs_passed, vals_passed

