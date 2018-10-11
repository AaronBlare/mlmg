from config.config import *
from infrastructure.load.top import *
from config.method import *
import pandas as pd
from infrastructure.save.features import save_features
import math


def get_butterfly_dict(config):

    method_metrics = get_method_metrics(config.method, config.is_clustering)

    config_f = Config(
        read_only=True,
        data_base=config.data_base,
        data_type=config.data_type,

        chromosome_type=config.chromosome_type,

        geo_type=config.geo_type,
        gene_data_type=config.gene_data_type,

        disease=config.disease,
        gender=Gender.F,
        scenario=config.scenario,
        approach=config.approach,
        method=config.method,

        is_clustering=config.is_clustering
    )

    config_m = Config(
        read_only=True,
        data_base=config.data_base,
        data_type=config.data_type,

        chromosome_type=config.chromosome_type,

        geo_type=config.geo_type,
        gene_data_type=config.gene_data_type,

        disease=config.disease,
        gender=Gender.M,
        scenario=config.scenario,
        approach=config.approach,
        method=config.method,

        is_clustering=config.is_clustering
    )

    keys = ['gene'] + method_metrics

    f_all_dict = load_top_dict(config_f, keys)
    m_all_dict = load_top_dict(config_m, keys)

    f_genes = f_all_dict['gene']
    m_genes = m_all_dict['gene']

    num_genes = len(f_genes)

    f_metrics = f_all_dict[get_method_main_metric(config.method)]
    m_metrics = m_all_dict[get_method_main_metric(config.method)]
    for gene_id in range(0, num_genes):
        f_metrics[gene_id] = metric_processing(config.method, f_metrics[gene_id])
        m_metrics[gene_id] = metric_processing(config.method, m_metrics[gene_id])

    f_metrics_passed = f_metrics
    m_metrics_passed = np.zeros(num_genes)
    metrics_diff = np.zeros(num_genes)
    for gene_id in range(0, num_genes):
        gene = f_genes[gene_id]
        m_id = m_genes.index(gene)
        m_metrics_passed[gene_id] = m_metrics[m_id]
        metrics_diff[gene_id] = f_metrics_passed[gene_id] - m_metrics_passed[gene_id]

    order = np.argsort(list(map(abs, metrics_diff)))[::-1]
    diff_srt = list(np.array(metrics_diff)[order])
    genes_srt = list(np.array(f_genes)[order])

    butterfly_dict = {'gene':genes_srt, 'diff': diff_srt}
    butterfly_df = pd.DataFrame(butterfly_dict)

    fn = 'butterfly_genes_' + 'method(' + config.method.value + ').xlsx'

    config_save = config_f
    # Solution
    config_save.scenario = Scenario.validation
    config_save.approach = config_f.approach
    config_save.method = Method.gender_specific
    # Attributes
    config_save.disease = config_f.disease
    config_save.gender = Gender.versus

    fn = get_result_path(config_save, fn)
    writer = pd.ExcelWriter(fn, engine='xlsxwriter')
    butterfly_df.to_excel(writer, index=False, sheet_name='butterfly')
    writer.save()

    return butterfly_dict


data_base = DataBase.GSE87571
data_type = DataType.gene

chromosome_type = ChromosomeTypes.non_gender

gene_data_type = GeneDataType.mean
geo_type = GeoType.islands_shores

disease = Disease.any

scenario = Scenario.approach
approach = Approach.top
method = Method.linreg

is_clustering = False

config = Config(
    read_only=True,

    data_base=data_base,
    data_type=data_type,

    chromosome_type=chromosome_type,

    gene_data_type=gene_data_type,
    geo_type=geo_type,

    disease=disease,

    scenario=scenario,
    approach=approach,
    method=method,

    is_clustering=is_clustering
)

get_butterfly_dict(config)
