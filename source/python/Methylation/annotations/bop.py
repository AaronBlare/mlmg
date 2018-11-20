import numpy as np
from annotations.gene import get_dict_cpg_gene
from annotations.conditions import *
from config.config import *
from infrastructure.path.path import *
import os.path
import pickle


def bop_condition(config, annotation):
    match = False
    if snp_condition(config, annotation):
        if chromosome_condition(config, annotation):
            if cpg_name_condition(config, annotation):
                if dna_region_condition(config, annotation):
                    if class_type_condition(config, annotation):
                        match = True
    return match


def get_dict_bop_cpgs(config):
    fn_pkl = 'dict_bop_cpgs.pkl'
    fn_pkl = get_data_path(config, fn_pkl)

    is_pkl = os.path.isfile(fn_pkl)
    if is_pkl:
        f = open(fn_pkl, 'rb')
        dict_bop_cpgs = pickle.load(f)
        f.close()
    else:
        dict_bop_cpgs = {}

        annotations = config.annotations

        cpg_names = annotations[Annotation.cpg.value]
        gene_names = annotations[Annotation.gene.value]
        chr = annotations[Annotation.chr.value]
        geo = annotations[Annotation.geo.value]
        map_info = annotations[Annotation.map_info.value]
        bop_names = annotations[Annotation.bop.value]
        class_type = annotations[Annotation.class_type.value]
        snp = annotations[Annotation.Probe_SNPs.value]
        snp1_10 = annotations[Annotation.Probe_SNPs_10.value]
        cross_reactive = annotations[Annotation.cross_reactive.value]
        for i in range(0, len(cpg_names)):

            curr_cpg = cpg_names[i]
            curr_gene = gene_names[i]
            curr_chr = chr[i]
            curr_geo = geo[i]
            curr_map_info = map_info[i]
            curr_bop = bop_names[i]
            curr_class_type = class_type[i]
            curr_snp = snp[i]
            curr_snp_10 = snp1_10[i]
            curr_cross_reactive = cross_reactive[i]

            annotation = {}
            annotation[Annotation.cpg.value] = curr_cpg
            annotation[Annotation.gene.value] = curr_gene
            annotation[Annotation.chr.value] = curr_chr
            annotation[Annotation.geo.value] = curr_geo
            annotation[Annotation.map_info.value] = curr_map_info
            annotation[Annotation.bop.value] = curr_bop
            annotation[Annotation.class_type.value] = curr_class_type
            annotation[Annotation.Probe_SNPs.value] = curr_snp
            annotation[Annotation.Probe_SNPs_10.value] = curr_snp_10
            annotation[Annotation.cross_reactive.value] = curr_cross_reactive

            if bop_condition(config, annotation):
                if len(curr_bop) > 0:
                    if curr_bop in dict_bop_cpgs:
                        dict_bop_cpgs[curr_bop].append(curr_cpg)
                    else:
                        dict_bop_cpgs[curr_bop] = [curr_cpg]

        # Sorting cpgs in bops by map_info
        num_bops = 0
        for curr_bop, curr_cpgs in dict_bop_cpgs.items():
            map_infos = []
            for curr_cpg in curr_cpgs:
                cpg_index = cpg_names.index(curr_cpg)
                curr_map_info = map_info[cpg_index]
                map_infos.append(curr_map_info)
            order = np.argsort(map_infos)
            cpgs_sorted = list(np.array(curr_cpgs)[order])
            dict_bop_cpgs[curr_bop] = cpgs_sorted
            num_bops += 1
            if num_bops % config.print_rate == 0:
                print('num_bops: ' + str(num_bops))

        # cross_reactive strict checking
        if config.cross_reactive is CrossReactiveType.cross_reactive_excluded:
            for curr_bop, curr_cpgs in dict_bop_cpgs.items():
                for curr_cpg in curr_cpgs:
                    cpg_index = cpg_names.index(curr_cpg)
                    curr_cross_reactive = cross_reactive[cpg_index]
                    if curr_cross_reactive == 1:
                        del dict_bop_cpgs[curr_bop]

        f = open(fn_pkl, 'wb')
        pickle.dump(dict_bop_cpgs, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return dict_bop_cpgs


def get_dict_bop_genes(config):
    dict_bop_cpgs = get_dict_bop_cpgs(config)

    fn_pkl = 'dict_bop_genes.pkl'
    fn_pkl = get_data_path(config, fn_pkl)

    is_pkl = os.path.isfile(fn_pkl)
    if is_pkl:
        f = open(fn_pkl, 'rb')
        dict_bop_genes = pickle.load(f)
        f.close()
    else:
        dict_bop_genes = {}
        dict_cpg_gene = get_dict_cpg_gene(config)
        for bop, cpgs in dict_bop_cpgs.items():
            genes = []
            for curr_cpg in cpgs:
                if curr_cpg in dict_cpg_gene:
                    curr_genes = dict_cpg_gene.get(curr_cpg)
                    genes += curr_genes
            if len(genes) > 0:
                dict_bop_genes[bop] = list(set(genes))

        f = open(fn_pkl, 'wb')
        pickle.dump(dict_bop_genes, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return dict_bop_genes