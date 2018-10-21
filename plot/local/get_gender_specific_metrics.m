function [names, metrics_1, metrics_2] = get_gender_specific_metrics(config)

metrics_id = get_metrics_id(config);

config.gender = 'F';
f_fn = sprintf('%s/data/%s/top.txt', ...
    config.up, ...
    get_result_path(config));
f_top_data = importdata(f_fn, ' ');
f_names = f_top_data.textdata;
f_metrics = f_top_data.data(:, metrics_id);
f_metrics = process_metrics(f_metrics, config);

config.gender = 'M';
m_fn = sprintf('%s/data/%s/top.txt', ...
    config.up, ...
    get_result_path(config));
m_top_data = importdata(m_fn, ' ');
m_names = m_top_data.textdata;
m_metrics = m_top_data.data(:, metrics_id);
m_metrics = process_metrics(m_metrics, config);

all_names = f_names;
num_names = size(all_names, 1);

f_metrics_passed = f_metrics;
m_metrics_passed = zeros(num_names, 1);
m_order = zeros(num_names, 1);
for id = 1:num_names
    f_gene = f_names(id);
    m_id = find(m_names==string(f_gene));
    m_metrics_passed(id) = m_metrics(m_id);
    m_order(id) = m_id;
    
    if mod(id, 1000) == 0
        id = id
    end
end

names = [];
metrics_1 = [];
metrics_2 = [];

if strcmp(config.method, 'linreg') && config.plot_method == 2
    
    p_value_lim = 1e-8;
    p_value_lim_log = -log10(p_value_lim);
    
    config_1 = config;
    config_1.metrics_rank = 2;
    
    metrics_id_1 = 2;
    f_metrics_1 = f_top_data.data(:, metrics_id_1);
    m_metrics_1 = m_top_data.data(:, metrics_id_1);
    m_metrics_1 = m_metrics_1(m_order);
    f_metrics_1 = process_metrics(f_metrics_1, config_1);
    m_metrics_1 = process_metrics(m_metrics_1, config_1);
    for id = 1:size(f_metrics_passed, 1)
        if(f_metrics_1(id) > p_value_lim_log) || (m_metrics_1(id) > p_value_lim_log)
            names = vertcat(names, all_names(id));
            metrics_1 = vertcat(metrics_1, f_metrics_passed(id));
            metrics_2 = vertcat(metrics_2, m_metrics_passed(id));
        end
        
        if mod(id, 1000) == 0
            id = id
        end
    end
    
elseif strcmp(config.method, 'manova') && config.plot_method == 2

    p_value_lim = 1e-8;
    p_value_lim_log = -log10(p_value_lim);
    
    for id = 1:size(f_metrics_passed, 1)
        if(f_metrics_passed(id) < p_value_lim_log) || (m_metrics_passed(id) < p_value_lim_log)
            names = vertcat(names, all_names(id));
            metrics_1 = vertcat(metrics_1, f_metrics_passed(id));
            metrics_2 = vertcat(metrics_2, m_metrics_passed(id));
        end
        
        if mod(id, 1000) == 0
            id = id
        end
    end
    
else
    
    names = all_names;
    metrics_1 = f_metrics_passed;
    metrics_2 = m_metrics_passed;
    
end

end