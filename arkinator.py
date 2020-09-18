import os
import time
import requests
import pandas as pd
from datetime import datetime

def holdings_to_csv(urls, loc):
    file_names = []
    for k,v in urls.items():
        resp = requests.get(v)
        csv_file = f"{loc}/csv/{k}.csv"
        file_names.append(csv_file)
        with open(os.path.join(os.getcwd(), csv_file), 'w') as f:
            f.write(resp.text)

    return file_names

def csvs_to_df(files, pkl_file):
    df = None
    for f in files:
        if not df is None:
            df = df.append(pd.read_csv(f)[:-3], ignore_index=True)
        else:
            df = pd.read_csv(f)[:-3]

    df.to_pickle(pkl_file)
    return df

if __name__ == '__main__':
    urls = {
        'arkk': 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv',
        'arkq': 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv',
        'arkw': 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv',
        'arkg': 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv',
        'arkf': 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv'
    }

    today = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    csv_files = holdings_to_csv(urls, 'data')
    df = csvs_to_df(csv_files, f"data/pkl/{today}.pkl")

    print(df)


