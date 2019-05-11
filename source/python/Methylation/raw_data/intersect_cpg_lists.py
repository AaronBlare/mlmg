import pandas as pd

def intersect_xlsx(files_names):

    keys = []

    data = dict()
    for file_name in files_names:
        key = file_name[:-5]
        keys.append(key)
        data[key] = []
        df = pd.read_excel(file_name)
        data[key].append(list(df.values))


    data_intersection = []
    data_column_names = []
    data_column_names.append('cpg')
    for key in keys:
        data_column_names.append(key[:8])
    for target_line in data[keys[0]][0]:
        cpg = target_line[0]
        for key in keys[1:]:
            for item in data[key][0]:
                if cpg == item[0] and list(item)[0:2] not in data_intersection:
                    item = list(item)[0:2]
                    data_intersection.append(item)

    fn = 'common' + keys[0][8:] + '.xlsx'
    df = pd.DataFrame(data_intersection)
    df = df.iloc[:, 0:2]
    #df.columns = data_column_names
    writer = pd.ExcelWriter(fn, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()

files_names = ['GSE40279_linreg.xlsx',
               'GSE87571_linreg.xlsx',
               'EPIC_linreg.xlsx']
intersect_xlsx(files_names)