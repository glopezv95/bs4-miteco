import pandas as pd

def get_df():

    df = pd.read_excel('data.xlsx', converters = {'contact_page': str})
    df.columns = [title.lower() for title in df.columns]

    size_list = [
        'Mediana', 'Gran empresa', 'Otros',
        'Entidad sin ánimo de lucro'
    ]

    df = df[
        (df['año'] == 2022) &
        (df['tamaño'].isin(size_list)) &
        (df['ccaa'].isin(['Madrid, Comunidad de', 'Galicia']))
    ].sort_values(by='año', ascending=False).reset_index(drop=True)

    return df