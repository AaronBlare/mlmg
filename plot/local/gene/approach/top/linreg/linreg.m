clear all;

age_ann = 'age';
gender_ann = 'gender';
disease_ann = 'disease';

base = 'GSE87571';
data_type = 'gene_data';

chromosome_type = 'non_gender';

geo_type = 'islands_shores';
gene_data_type = 'mean';

info_type = 'result';

disease = 'any';
gender = 'M';
scenario = 'approach';
approach = 'top';
method = 'linreg';

gene = 'OFD1';

up = '../../../../../..';

fn = sprintf('%s/data/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/top.txt', ...
    up, ...
    base, ...
    data_type, ...
    chromosome_type, ...
    geo_type, ...
    gene_data_type, ...
    info_type, ...
    disease, ...
    gender, ...
    scenario, ...
    approach, ...
    method);

top_data = importdata(fn);

genes = top_data.textdata;
slopes = top_data.data(:, 5);
intercepts = top_data.data(:, 6);

fn = sprintf('%s/data/%s/attributes.txt', up, base);
ann = importdata(fn);

keys = strsplit(string(ann{1}), ' ')';
age_id = 0;
gender_id = 0;
disease_id = 0;
for key_id = 1:size(keys, 1)
    if string(keys{key_id}) == string(age_ann)
        age_id = key_id;
    end
    if string(keys{key_id}) == string(gender_ann)
        gender_id = key_id;
    end
    if string(keys{key_id}) == string(disease_ann)
        disease_id = key_id;
    end
end

indexes = [1:size(ann, 1)-1]';

if gender_id > 0  
    genders = [];
    for id = 2:size(ann, 1)
        vals = strsplit(string(ann{id}), ' ')';
        curr_ann = string(vals{gender_id});
        genders = vertcat(genders, curr_ann);
    end
    
    if ~strcmp(string(gender), 'any')
        curr_indexes = [];
        for id = 1:size(genders, 1)
            if strcmp(genders(id), gender)
                curr_indexes = vertcat(curr_indexes, id);
            end
        end
        tmp_indexes = intersect(indexes, curr_indexes);
        indexes = tmp_indexes;
    end
end

if disease_id > 0
    diseases = [];
    for id = 2:size(ann, 1)
        vals = strsplit(string(ann{id}), ' ')';
        curr_ann = string(vals{disease_id});
        diseases = vertcat(diseases, curr_ann);
    end
    
    if ~strcmp(string(disease_type), 'any')
        curr_indexes = [];
        for id = 1:size(diseases, 1)
            if strcmp(diseases(id), disease_type)
                curr_indexes = vertcat(curr_indexes, id);
            end
        end
        tmp_indexes = intersect(indexes, curr_indexes);
        indexes = tmp_indexes;
    end
end

ages = zeros(size(ann, 1)-1, 1);
for id = 2:size(ann, 1)
    vals = strsplit(string(ann{id}), ' ')';
    curr_ann = str2double(string(vals{age_id}));
    ages(id-1) = curr_ann;
end

ages_passed = zeros(size(indexes, 1), 1);
for id = 1:size(indexes, 1)
    index = indexes(id);
    ages_passed(id) = ages(index);
end

fn = sprintf('%s/data/%s/%s/%s/%s/%s/%s/gene_data.txt', ...
    up, ...
    base, ...
    data_type, ...
    chromosome_type, ...
    geo_type, ...
    gene_data_type, ...
    'data');

data = importdata(fn);
genes_names = data.textdata;
genes_data = data.data;

gene_name = string(gene);
idx = find(genes_names==gene_name);
gene_data = genes_data(idx, :)';

gene_data_passed = size(indexes, 1);
for id = 1:size(indexes, 1)
    gene_data_passed(id) = gene_data(indexes(id));
end

gene_id = find(genes==gene_name);

slope = slopes(gene_id);
intercept = intercepts(gene_id);
x_lin = [min(ages), max(ages)];
y_lin = [slope * x_lin(1) + intercept, slope * x_lin(2) + intercept];

figure
hold all;
h = plot(ages_passed, gene_data_passed, 'o', 'MarkerSize', 10, 'MarkerFaceColor', 'w');
set(get(get(h, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');
color = get(h, 'Color');

hold all;
h = plot(x_lin, y_lin, '-', 'LineWidth', 3);
legend(h, sprintf('%s: %s', gene_name, gender));
set(h, 'Color', color)
set(gca, 'FontSize', 30);
xlabel('age', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel('$\beta$', 'Interpreter', 'latex');

box on;




