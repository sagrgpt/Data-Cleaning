import pandas as pd
import numpy as np

def processMainDataset():
    # Reading the main dataset
    df = pd.read_excel('rate_sheet.xlsx','Table 1')
    del df['Country']
    del df['ROUTING']
    del df['POD']
    df['special remarks'] = df['special remarks'].fillna('')
    df['remarks'] += ' '+df['special remarks']
    del df['special remarks']
    df['VALIDITY'] = df.VALIDITY.dt.strftime('%m-%d-%Y')
    return df

def processLookupDataset():
    df = pd.read_csv("lookup (3).csv",names=['p_name','p_code','country'])
    df = df.drop_duplicates(subset="p_code")
    return df
