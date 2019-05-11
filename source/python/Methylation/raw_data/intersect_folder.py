import pandas as pd


path = 'variance'
files_names = ['GSE40279.xlsx', 'GSE87571.xlsx', 'EPIC.xlsx']
files_pathes = [path + '\\' + file_name for file_name in files_names]

cpg_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
gene_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
for file_id in range(0, len(files_names)):
    file_name = files_names[file_id][:-5]
    file_path = files_pathes[file_id]
    df = pd.read_excel(file_path)
    cpg_dict[file_name] = list(df.item)
    gene_dict[file_name] = list(df.aux)

i_cpgs = set(cpg_dict[files_names[0][:-5]])
for file_id in range(1, len(files_names)):
    file_name = files_names[file_id]
    cpg_data = cpg_dict[file_name[:-5]]
    i_cpgs = set(i_cpgs.intersection(cpg_data))

i_cpgs = list(i_cpgs)

# Table for intersection
i_dict = {}
i_dict['cpg'] = []
i_dict['gene'] = []

for f_id in range(0, len(i_cpgs)):
    cpg = i_cpgs[f_id]
    i_dict['cpg'].append(cpg)
    gene_id = cpg_dict[files_names[0][:-5]].index(cpg)
    gene = gene_dict[files_names[0][:-5]][gene_id]
    i_dict['gene'].append(gene)


i_df = pd.DataFrame(i_dict)
name = '_'.join([file_name[:-5] for file_name in files_names])
writer = pd.ExcelWriter(path + '\\' + name + '.xlsx', engine='xlsxwriter')
i_df.to_excel(writer, index=False, sheet_name='i')
writer.save()

