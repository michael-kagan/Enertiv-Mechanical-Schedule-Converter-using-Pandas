import pandas as pd
import numpy as np
import json
import pandas.io.formats.excel

def make_schedule(filename):

    with open('/home/mkagan/mysite/' + filename, encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    ewm = df[df.astype(str)['equipmentmetadata_set'] != '[]']


    ewm = ewm.drop(['traced', 'channels', 'created', 'modified', 'id'], axis=1)
    ewm = ewm.rename(columns={'name' : 'equipment name'})


    ewm = ewm.explode('equipmentmetadata_set')


    ewm.reset_index(drop=True, inplace=True)

    # Replace NaN by empty dict
    def replace_nans_with_dict(series):
        for idx in series[series.isnull()].index:
            series.at[idx] = {}
        return series


    # Explodes list and dicts
    def df_explosion(df, col_name:str):
        if df[col_name].isna().any():
            df[col_name] = replace_nans_with_dict(df[col_name])
        df.reset_index(drop=True, inplace=True)
        df1 = pd.DataFrame(df.loc[:,col_name].values.tolist())
        df = pd.concat([df,df1], axis=1)
        df.drop([col_name], axis=1, inplace=True)
        return df


    ewm = df_explosion(ewm, 'equipmentmetadata_set')


    ewm = ewm.drop(['parent_equipment', 'sublocation', 'id', 'equipment'], axis=1)
    ewm = ewm.drop(['equipment_metadata_category', 'location_attachment', 'url', 'created', 'modified', 'tag_type', 'units', 'description'], axis=1)

    cols = ewm[ewm['equipment name']==ewm['equipment name'][:len(ewm['equipment name'])]].name.tolist()

    # remove duplicates in the list of columns
    def remove_dups(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    cols = remove_dups(cols)

    ewm_pivot = pd.pivot(ewm, index='equipment name', columns='name', values='value')[cols]


    writer = pd.ExcelWriter(filename + '.xlsx')
    workbook = writer.book


    i = 0

    for qw, x in ewm_pivot.groupby(ewm_pivot.isnull().dot(ewm_pivot.columns)):
        x = x.dropna(1)
        x.to_excel(writer, sheet_name=filename, startrow=i)
        worksheet = writer.sheets[filename]
        i += (len(x.index) + 5)

    writer.save()

    return writer


