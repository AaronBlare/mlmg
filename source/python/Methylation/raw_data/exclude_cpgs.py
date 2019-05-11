import pandas as pd


path = '2019_02'
files_names = ['GSE40279_2.xlsx', 'GSE40279_1.xlsx']
files_pathes = [path + '\\' + file_name for file_name in files_names]

cpg_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
gene_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
for file_id in range(0, len(files_names)):
    file_name = files_names[file_id][:-5]
    file_path = files_pathes[file_id]
    df = pd.read_excel(file_path)
    cpg_dict[file_name] = list(df.item)
    gene_dict[file_name] = list(df.aux)

main_cpgs = set(cpg_dict[files_names[0][:-5]])
main_cpgs = list(main_cpgs)

exclude_cpgs = set(cpg_dict[files_names[1][:-5]])
exclude_cpgs = list(exclude_cpgs)

main_cpgs = [cpg for cpg in main_cpgs if cpg not in exclude_cpgs]

# Table for intersection
i_dict = {}
i_dict['item'] = []
i_dict['aux'] = []

for f_id in range(0, len(main_cpgs)):
    cpg = main_cpgs[f_id]
    i_dict['item'].append(cpg)
    gene_id = cpg_dict[files_names[0][:-5]].index(cpg)
    gene = gene_dict[files_names[0][:-5]][gene_id]
    i_dict['aux'].append(gene)


i_df = pd.DataFrame(i_dict)
writer = pd.ExcelWriter(path + '\\' + files_names[0][0:3] + '_ex.xlsx', engine='xlsxwriter')
i_df.to_excel(writer, index=False, sheet_name='i')
writer.save()

