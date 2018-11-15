function fn = get_result_path(config)
fn = '';
if strcmp(config.data_type, 'gene_data')
    fn = sprintf('%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s', ...
        config.data_base, ...
        config.data_type, ...
        config.cross_reactive, ...
        config.snp, ...
        config.chromosome_type, ...
        config.geo_type, ...
        config.gene_data_type, ...
        config.info_type, ...
        config.scenario, ...
        config.approach, ...
        config.method, ...
        config.disease, ...
        config.gender);
elseif strcmp(config.data_type, 'cpg_data')
    fn = sprintf('%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s', ...
        config.data_base, ...
        config.data_type, ...
        config.cross_reactive, ...
        config.snp, ...
        config.chromosome_type, ...
        config.dna_region, ...
        config.info_type, ...
        config.scenario, ...
        config.approach, ...
        config.method, ...
        config.disease, ...
        config.gender);
elseif strcmp(config.data_type, 'attributes')
    fn = sprintf('%s/%s', ...
        config.data_base, ...
        config.data_type);
elseif strcmp(config.data_type, 'bop_data')
    fn = sprintf('%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s', ...
        config.data_base, ...
        config.data_type, ...
        config.cross_reactive, ...
        config.snp, ...
        config.chromosome_type, ...
        config.class_type, ...
        config.info_type, ...
        config.scenario, ...
        config.approach, ...
        config.method, ...
        config.disease, ...
        config.gender);
end
end