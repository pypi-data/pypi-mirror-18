#!/usr/bin/env python
# -*- coding:utf-8 -*- 

'''
Created on 2016年12月2日
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
'''
import tushare as ts

import pandas as pd

# def global_index():
#     df = global_realtime()
#     df = df.set_index('symbol')
#     af = get_area_map()[['symbol', 'area']]
#     af = af.set_index('symbol')
#     df = df.merge(af, left_index=True, right_index=True)[['name', 'price', 'chgp', 'area']]
#     df['chgp'] = df['chgp'].astype(float)
#     df['chgp'] = df['chgp'].map(ct.FORMAT)
#     datastr = ''
#     for idx in df.index:
#         row = df.ix[idx]
#         rowstr = '{name:"%s",value:%s,price:%s,label:"%s"}'%(row['area'], row['chgp'], row['price'], row['name'])
#         datastr += rowstr + ',\n'
#     print(datastr)

def get_area_map():
    df = pd.read_csv('../data/glo.csv', encoding='gbk')
    return df


def make_k_data():
    df = ts.get_k_data('600000', start='2015-01-01')
    datastr = ''
    for idx in df.index:
        rowstr = '[\'%s\',%s,%s,%s,%s]' % (df.ix[idx]['date'], df.ix[idx]['open'], 
                                           df.ix[idx]['close'], df.ix[idx]['low'], 
                                           df.ix[idx]['high'])
        datastr += rowstr + ',\n'
    print(datastr)
        
    
if __name__ == '__main__':
    make_k_data()