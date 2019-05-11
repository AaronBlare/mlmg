from infrastructure.load.top import *
import pandas as pd

num_top = 100

path = 'GSE87571'
files_names = ['bop_F.xlsx', 'bop_M.xlsx']
files_pathes = [path + '\\' + file_name for file_name in files_names]

f_dict = dict()
m_dict = dict()
for file_id in range(0, len(files_names)):
    file_name = files_names[file_id]
    file_path = files_pathes[file_id]
    if file_name[4] == 'F':
        df = pd.read_excel(file_path, header=None, names=['names'])
        f_dict['gene'] = list(df.names)
    if file_name[4] == 'M':
        df = pd.read_excel(file_path, header=None, names=['names'])
        m_dict['gene'] = list(df.names)


f_genes = f_dict['gene'][0:num_top]
m_genes = m_dict['gene'][0:num_top]

i_genes = list(set(f_genes).intersection(m_genes))
only_f_genes = list(set(f_genes) - set(i_genes))
only_m_genes = list(set(m_genes) - set(i_genes))

# Table for female-only
only_f_dict = {}
only_f_dict['gene'] = []
only_f_dict['top'] = []
only_f_dict['top_vs'] = []

for f_id in range(0, len(only_f_genes)):
    gene = only_f_genes[f_id]
    gene_id = f_dict['gene'].index(gene)
    is_in_vs = True if gene in m_dict['gene'] else False
    if is_in_vs:
        gene_id_vs = m_dict['gene'].index(gene)
    else:
        gene_id_vs = -1

    only_f_dict['gene'].append(gene)
    only_f_dict['top'].append(gene_id)
    if is_in_vs:
        only_f_dict['top_vs'].append(gene_id_vs)
    else:
        only_f_dict['top_vs'].append('None')

only_f_order = np.argsort(only_f_dict['top'])
only_f_dict['gene'] = list(np.array(only_f_dict['gene'])[only_f_order])
only_f_dict['top'] = list(np.array(only_f_dict['top'])[only_f_order])
only_f_dict['top_vs'] = list(np.array(only_f_dict['top_vs'])[only_f_order])

only_f_df = pd.DataFrame(only_f_dict)

# Table for male-only
only_m_dict = {}
only_m_dict['gene'] = []
only_m_dict['top'] = []
only_m_dict['top_vs'] = []

for f_id in range(0, len(only_m_genes)):
    gene = only_m_genes[f_id]
    gene_id = m_dict['gene'].index(gene)
    is_in_vs = True if gene in f_dict['gene'] else False
    if is_in_vs:
        gene_id_vs = f_dict['gene'].index(gene)
    else:
        gene_id_vs = -1

    only_m_dict['gene'].append(gene)
    only_m_dict['top'].append(gene_id)
    if is_in_vs:
        only_m_dict['top_vs'].append(gene_id_vs)
    else:
        only_m_dict['top_vs'].append('None')

only_m_order = np.argsort(only_m_dict['top'])
only_m_dict['gene'] = list(np.array(only_m_dict['gene'])[only_m_order])
only_m_dict['top'] = list(np.array(only_m_dict['top'])[only_m_order])
only_m_dict['top_vs'] = list(np.array(only_m_dict['top_vs'])[only_m_order])

only_m_df = pd.DataFrame(only_m_dict)

# Table for intersection
i_dict = {}
i_dict['gene'] = []
i_dict['top_f'] = []
i_dict['top_m'] = []

for f_id in range(0, len(i_genes)):
    gene = i_genes[f_id]
    gene_id_f = f_dict['gene'].index(gene)
    gene_id_m = m_dict['gene'].index(gene)

    i_dict['gene'].append(gene)
    i_dict['top_f'].append(gene_id_f)
    i_dict['top_m'].append(gene_id_m)

i_order = np.argsort(i_dict['top_f'])
i_dict['gene'] = list(np.array(i_dict['gene'])[i_order])
i_dict['top_f'] = list(np.array(i_dict['top_f'])[i_order])
i_dict['top_m'] = list(np.array(i_dict['top_m'])[i_order])

i_df = pd.DataFrame(i_dict)

writer = pd.ExcelWriter(path + '\\' + files_names[0][0:3] + '_I.xlsx', engine='xlsxwriter')
only_f_df.to_excel(writer, index=False, sheet_name='only_f')
only_m_df.to_excel(writer, index=False, sheet_name='only_m')
i_df.to_excel(writer, index=False, sheet_name='i')
writer.save()

