import os
import time
import pandas as pd
from datetime import datetime

def last_two_files(d):
    files = []
    for f in os.listdir(d):
        files.append(f"{d}/{f}")
    
    return sorted(files[-2:], reverse=True)

def get_funds(df):
    return df.fund.unique().tolist()

def get_tickers(df):
    return df.ticker.unique().tolist()

def compare(df, funds, tickers):
    results = []
    base_columns = ['date', 'fund', 'company', 
        'ticker', 'cusip', 'shares', 'market value($)', 'weight(%)']

    for fund in funds:
        df_fund = df.loc[df['fund'] == fund]
        for t in tickers:
            df_t = df_fund.loc[df_fund['ticker'] == t]
            if df_t.shape[0] == 2:
                shares = df_t['shares'].diff().tolist()[1]
                if shares != 0.0:
                    cap = df_t['market value($)'].diff().tolist()[1]
                    weight = df_t['weight(%)'].diff().tolist()[1]
                    row = df_t.iloc[-1].tolist()
                    new_row = []
                    for i in row:
                        new_row.append(str(i))
                    new_row.extend([str(round(shares, 2)), str(round(cap, 2)), str(round(weight, 4))])
                    results.append(new_row)

    return results

def save_to_file(loc, cols, data):
    with open(loc, 'w') as f:
        f.write(','.join(cols)+'\n')
        for line in data:
            f.write(','.join(line)+'\n')


if __name__ == '__main__':
    file_dir = os.path.join(os.getcwd(), 'data/pkl')
    files = last_two_files(file_dir)

    df = pd.read_pickle(files.pop()).append(pd.read_pickle(files.pop()), ignore_index=True)
    
    funds = get_funds(df)
    tickers = get_tickers(df)
    comp = compare(df, funds, tickers)
    columns = ['date', 'fund', 'company', 'ticker', 
        'cusip', 'shares', 'market cap', 'weight', 
        'shares_diff', 'cap_diff', 'weight_diff']
    save_to_file('data/output/changes.csv', columns, comp)
    