# -*- coding: utf-8 -*-
import collections
from collections import defaultdict
import sys
import os
import logging
import xlrd
import pandas as pd
import datetime
import re
import tmp_pickle
import pickle
import numpy as np
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def getTheFile(filename, this_file=__file__):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))


####获取数据存成pkl
def getExcel(filepaths):
    filename = getTheFile(filepaths)
    data = xlrd.open_workbook(filename)
    sheet_len = len(data.sheets())
    table = data.sheets()[0]
    header = table.row_values(0)
    header.append('date')
    ###
    ###读取所有数据到dataframe dff中
    dff = pd.DataFrame(columns = header)
    for j in range(0,sheet_len):
        ret = {
            'header': [],
            'data': []
        }
        sheet_name = data.sheets()[j].name
        table = data.sheets()[j]  # 通过索引顺序获取
        # table = data.sheet_by_index(0)  # 通过索引顺序获取
        # table = data.sheet_by_name(u'Sheet')  # 通过名称获取
        nrows = table.nrows
        print (nrows)
        #ncols = table.ncols
        if nrows>1:
            for i in range(1,nrows):
                rows = table.row_values(i)
                rows.append(sheet_name)
                ret['data'].append(rows)

            df = pd.DataFrame(ret['data'])
            df.columns = [header]

            dff = dff.append(df, ignore_index=True)
            dff['持有or卖出备注:1or0'] = dff['持有or卖出备注:1or0'].astype('int64')
    df_data = dff.sort_values(by=['code','date'])
    df_data = df_data.groupby(['code'])

    tmp_pickle.wpicke('../pkl/save_data_final_0205.pkl', df_data)



####根据pkl的数据生成想要的分段时间数据
def getDetail(filepath):
    df_data = tmp_pickle.rpicke(filepath)
    ####
    ####根据需求获取想要的数据
    df_writer = pd.DataFrame()
    ret2 = {
        'header': [],
        'data': []
    }
    for code, groups in df_data:
        #if code == '1':
            groups = groups[groups['code'].isin([code])]
            buy_in = groups[groups['持有or卖出备注:1or0'].isin([1])]#买入
            pur_out = groups[groups['持有or卖出备注:1or0'].isin([0])]#卖出
            pur_len = len(pur_out)  # 每支股票有几个卖出
            buy_len = len(buy_in)
            print (buy_len)
            if pur_len > 0:
                #卖出的最后一天做标记
                last_pur_day = pur_out['date'].values[-1]
                #最后一天买入做标记
                last_open_day = ''

                ###计算买入日期start
                buy_date_len = buy_in['date'].shape[0]
                ret_data = []
                tmp_date = []
                today = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
                temp_open_date = today
                for j in range(pur_len):
                    ret_tmp = []
                    pur_date = pur_out['date'][j:j + 1].values[0]
                    pur_date  = datetime.datetime.strptime(pur_date,'%Y-%m-%d')
                    for i in range(buy_date_len):
                        buy_date = buy_in['date'][i:i + 1].values[0]
                        buy_date = datetime.datetime.strptime(buy_date, '%Y-%m-%d')
                        if buy_date < pur_date and buy_date not in tmp_date and temp_open_date !=None and buy_date > temp_open_date:
                            open_date = buy_date
                            tmp_date.append(open_date)
                            open_date = open_date.strftime('%Y-%m-%d')
                            ret_tmp.append(code)
                            new_date = ''
                            if '@' in code:
                                code_new = code
                                code_new = code_new[-10:]
                                open_date = code_new
                                new_date = open_date
                            if new_date !=  '' and new_date !=open_date:
                                open_date = new_date
                            temp_open_date = pur_date
                            ret_tmp.append(open_date)
                            xian_cang = buy_in['现仓位'][i:i + 1].values[0]
                            print('xian_cang1',xian_cang)
                            ret_tmp.append(xian_cang)
                            open_val = buy_in['open'][i:i + 1].values[0]
                            ret_tmp.append(open_val)
                            break

                    if len(ret_tmp)==4:
                        ret_data.append(ret_tmp)

                    if j == pur_len-1:
                        last_open_day= ret_tmp[1]

                ###计算买入日期end


                high_val = pur_out['最高收盘价']
                out_val = pur_out['卖出价']
                out_date = pur_out['date']
                df = pd.DataFrame([high_val, out_val, out_date])
                cols = len(ret_data)
                for j in range(cols):
                    tmp_list = []
                    tmp_list.extend(ret_data[j])
                    for i in range(3):
                        tmp_list.append(df.values.tolist()[i][j])
                    ret2['data'].append(tmp_list)

                last_pur_day = datetime.datetime.strptime(last_pur_day,'%Y-%m-%d').strftime('%Y-%m-%d')
                # last_open_day = datetime.datetime.strptime(last_open_day, '%Y-%m-%d').strftime('%Y-%m-%d')
                # last_out_day = out_date.values[-1]
                buy_in = buy_in.loc[(buy_in['date']>last_pur_day)]
                buy_len = len(buy_in)
                pur_len = 0
                print(buy_len)
            if pur_len == 0 and buy_len>0:
                code = code
                open_date = buy_in['date'][0:1].values[0]
                if '@' in code:
                    code_new = code
                    code_new = code_new[-10:]
                    open_date = code_new
                xian_cang = buy_in['现仓位'][0:1].values[0]
                open_val = buy_in['open'][0:1].values[0]
                high_val = buy_in['最高收盘价'][0:1].values[0]
                out_val = 0
                out_date = '无卖出'
                tmp_buy = []
                tmp_buy.append(code)
                tmp_buy.append(open_date)
                tmp_buy.append(xian_cang)
                tmp_buy.append(open_val)
                tmp_buy.append(high_val)
                tmp_buy.append(out_val)
                tmp_buy.append(out_date)
                ret2['data'].append(tmp_buy)

    #print (ret2['data'])
    header = ['code', '买入日','现仓位', '买入价', '最高收盘价', '卖出价','卖出日']
    df_tmp = pd.DataFrame(ret2['data'])
    df_tmp.columns = [header]
    df_writer = df_writer.append(df_tmp,ignore_index=True)
    writer = pd.ExcelWriter('../output/output_老B1+老B2-4天_明细0205.xlsx')
    df_writer.to_excel(writer, 'Sheet1')
    writer.save()


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    # filepaths = '../input/老B1+老B2-4天_明细0205.xlsx'
    # getExcel(filepaths)
    filepath = '../pkl/save_data_final_0205.pkl'
    getDetail(filepath)