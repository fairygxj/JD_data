# -*- coding: utf-8 -*-
import sys
import os
import logging
import xlrd
import pandas as pd
import datetime
import math
import time
import tmp_pickle
from numpy import NaN
import numpy as np
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#####
#####解析分时的明细的操作信号 最新的 修改手续费后 参数后 0302



#说明price1_new =

###手续费
BUY_RATE = 1.0005
PUR_RATE = 0.9985   ####0.0015
stock_position_number =0.2

def getTheFile(filename, this_file=__file__):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))


###
###
##### 解析时间
def getList(list_opentime,list_pingtime):
    len_opentime = len(list_opentime)
    len_pingtime = len(list_pingtime)
    if len_opentime == 1:
        list_opentime[0] = list_opentime[0].lstrip('[').rstrip(']')
        list_opentime[0] = list_opentime[0].strip('\'')
    if len_pingtime == 1:
        list_pingtime[0] = list_pingtime[0].lstrip('[').rstrip(']')
        list_pingtime[0] = list_pingtime[0].strip('\'')
    if len_opentime == 2:
        list_opentime[0] = list_opentime[0].lstrip('[')
        list_opentime[0] = list_opentime[0].strip('\'')
        list_opentime[-1] = list_opentime[-1].rstrip(']')
        list_opentime[-1] = list_opentime[-1].strip(' ').strip('\'')

    if len_pingtime == 2:
        list_pingtime[0] = list_pingtime[0].lstrip('[')
        list_pingtime[0] = list_pingtime[0].strip('\'')
        list_pingtime[-1] = list_pingtime[-1].rstrip(']')
        list_pingtime[-1] = list_pingtime[-1].strip(' ').strip('\'')
    return list_opentime,list_pingtime

def add_A(m,sheet_name):
    if len(m) == 19:
        k = m+'B'
    else:
        k = ''
    return k

def add_B(m,sheet_name):
    if len(m) == 19:
        k = m+'S'
    elif m == '该股最后一天':
        k = sheet_name + ' 15:00:00S'
    else:
        k = ''
    return k

def get_not_ten(standard):
    """仓位数四舍五入十位 返回 0.2*标仓 """
    return round(stock_position_number * standard / 100) * 100

##
###
###  ##生成数据pkl
def getExcel(filpath):
    filename = getTheFile(filpath)
    data = xlrd.open_workbook(filename)
    sheet_len = len(data.sheets())
    table = data.sheets()[0]
    header = table.row_values(0)
    header.append('price1_new')
    header.append('price2_new')
    header.append('price3_new')
    header.append('price4_new')
    header.append('date')

    ####这四列一一对应出现
    header.append('开仓平仓时间')
    header.append('价格')
    header.append('新价格')
    header.append('标签')
    ####这四列一一对应出现
    header.append('标仓2')
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
        #print ('nrows',nrows)
        #ncols = table.ncols
        if nrows>1:
            for i in range(1,nrows):#从第二行开始忽略掉表头
                list_time = [] #开平仓时间列表
                list_price = [] #原始操作价格列表
                list_price_new = []#处理后的价格列表
                list_label = [] #标签列表
                list_cang = []#
                rows = table.row_values(i)
                rows.append('')
                rows.append('')
                rows.append('')
                rows.append('')
                rows.append(sheet_name)
                #print (rows)
                rows[7] =str(rows[7])#开仓时间有的是0  float类型  需要转换
                rows[8] = str(rows[8])  # 平仓时间有的是0  float类型  需要转换
                list_opentime = rows[7].split(',')
                list_pingtime = rows[8].split(',')
                list_opentime,list_pingtime = getList(list_opentime,list_pingtime)

                ###获取每条记录的开仓平仓时间，合并为一个list 注意是每条记录不是每个code
                list_opentime = list(add_A(i,sheet_name) for i in list_opentime)
                list_pingtime = list(add_B(j,sheet_name) for j in list_pingtime)
                list_time.extend(list_opentime)
                list_time.extend(list_pingtime)
                list_time = sorted(list_time)
                while '' in list_time:
                    print('LIST里面有空格################################', list_time)
                    list_time.remove('')

                len_listtime = 0  # 开仓时间平仓时间每个code每天的长度
                if list_time != None:
                    len_listtime = len(list_time)
                if rows[10] != '':
                    rows[14] = rows[10] * rows[2] * 0.2
                if rows[11] != '':
                    rows[15] = rows[11] * rows[2] * 0.2
                if rows[12] != '':
                    rows[16] = rows[12] * rows[2] * 0.2
                if rows[13] != '':
                    rows[17] = rows[13] * rows[2] * 0.2
                if len_listtime == 1:
                    list_price.append(rows[10])
                    list_price_new.append(rows[14])
                    list_cang.append(rows[2])#标仓
                if len_listtime == 2:
                    list_price.append(rows[10])
                    list_price.append(rows[11])
                    list_price_new.append(rows[14])
                    list_price_new.append(rows[15])
                    list_cang.append(rows[2])#标仓
                    list_cang.append(rows[2])#标仓
                if len_listtime == 3:
                    list_price.append(rows[10])
                    list_price.append(rows[11])
                    list_price.append(rows[12])
                    list_price_new.append(rows[14])
                    list_price_new.append(rows[15])
                    list_price_new.append(rows[16])
                    list_cang.append(rows[2])  # 标仓
                    list_cang.append(rows[2])  # 标仓
                    list_cang.append(rows[2])  # 标仓
                if len_listtime == 4:
                    list_price.append(rows[10])
                    list_price.append(rows[11])
                    list_price.append(rows[12])
                    list_price.append(rows[13])
                    list_price_new.append(rows[14])
                    list_price_new.append(rows[15])
                    list_price_new.append(rows[16])
                    list_price_new.append(rows[17])
                    list_cang.append(rows[2])  # 标仓
                    list_cang.append(rows[2])  # 标仓
                    list_cang.append(rows[2])  # 标仓
                    list_cang.append(rows[2])  # 标仓

                #####
                ##### ##生成标志位的list start
                if list_time != None:
                    for m in list_time:
                        list_label.append(m[-1])
                #####
                ##### ##生成标志位end

                # if list_time == None:
                #     list_time = NaN
                # if len(list_price) == 0:
                #     list_price = NaN

                if len(list_price) != len_listtime or len(list_label) != len_listtime:
                    print('ERROR LENGTH!!!!!!!!!!!!!')
                rows[7] = list_opentime
                rows[8] = list_pingtime
                rows.append(list_time)
                rows.append(list_price)
                rows.append(list_price_new)
                rows.append(list_label)
                rows.append(list_cang)
                ret['data'].append(rows)
            print (header)
            print (ret['data'])
            df = pd.DataFrame(ret['data'])
            df.columns = [header]
            dff = dff.append(df, ignore_index=True)
    #print (dff)
    df_data = dff.sort_values(by=['code','date'])
    df_data = df_data.groupby(['code'])
    today = time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))
    print(today)
    tmp_pickle.wpicke('../pkl/{}老B1+老B2-4天fromDtoM_detail.pkl'.format(today), df_data)

'''
根据李杰信号生成价格比较
'''
def getDetail(filepathes):
    df_data = tmp_pickle.rpicke(filepathes)
    ####根据需求获取想要的数据
    df_writer = pd.DataFrame()
    ret_buy = {
        'header': [],
        'data': []
    }
    ret_sell = {
        'header': [],
        'data': []
    }
    header = ['code','开仓平仓时间','price1_new','biao_cang','price1_new_time','price2_new','price2_new_time','price1','price2','最高盈利1','out5day','out10day']
    ret_buy['header'] = header
    ret_sell['header'] = header
    for code, groups in df_data:
        #if code=='153':
            groups = groups[groups['code'].isin([code])]
            #groups = groups.dropna(subset=["开仓平仓时间"])
            #groups = groups.dropna(subset=["价格"])
            time_len = len(groups)  # 每支股票的记录数
            if time_len!=0:
                list_time = groups['开仓平仓时间']
                list_price = groups['价格']
                #list_price_new = groups['新价格']
                list_label = groups['标签']
                list_cang = groups['标仓2']
                #biao_cang = groups['标仓']
                # biao_cang = np.array(biao_cang)
                # biao_cang = biao_cang[0]
                list_time = np.array(list_time)
                list_cang = np.array(list_cang)

                list_label = list(np.array(list_label))

                #print ('wwwwwwwwwwwwwwwwwbiao_cang',biao_cang)
                list_time_bak = []
                list_price_bak = []
                #list_price_new_bak = []
                list_label_bak = []
                list_cang_bak = []
                for i in list_time:
                    list_time_bak.extend(i)
                # print('wwwwwwwwwwwwwwwww', list_time_bak)
                # print('wwwwwwwwwwwwwwwww', len(list_time_bak))
                for j in list_price:
                    list_price_bak.extend(j)
                # for m in list_price_new:
                #     list_price_new_bak.extend(m)
                for n in list_label:
                    list_label_bak.extend(n)
                for a in list_cang:
                    list_cang_bak.extend(a)


                ####原始价格列表
                if len(list_price_bak) % 2 != 0:
                    list_price_bak.append(list_price_bak[-1])
                    #del(list_price_bak[-1])

                ####新价格列表  可以不用
                # if len(list_price_new_bak) % 2 != 0:
                #     list_price_new_bak.append(list_price_new_bak[-1])
                    #del(list_price_new_bak[-1])

                #时间列表
                if len(list_time_bak) % 2 != 0:
                    list_time_bak.append(list_time_bak[-1])
                    #del(list_time_bak[-1])

                # 标签列表
                if len(list_label_bak) % 2 != 0:
                    list_label_bak.append(list_label_bak[len(list_label_bak) - 1])
                    #del(list_label_bak[-1])

                # 标仓列表
                if len(list_cang_bak) % 2 != 0:
                    list_cang_bak.append(list_cang_bak[len(list_cang_bak) - 1])
                    #del(list_cang_bak[-1])

                ####
                ####
                len_price = len(list_price_bak)
                if len_price >= 1:
                    count = 0
                    for m in range(0,len_price,2):
                        left = 0 + count * 2
                        right = 1 + count * 2
                        price1 = float(list_price_bak[left])
                        price2 = float(list_price_bak[right])
                        biao_cang = list_cang_bak[left]
                        biao_cang2 = get_not_ten(biao_cang)
                        price1_new = price1 * biao_cang2
                        price1_time = list_time_bak[left]
                        price2_new = price2 * biao_cang2
                        price2_time = list_time_bak[right]
                        price21 = 0.0

                        out5 = None
                        out10 = None


                        if list_label_bak[left] == 'S' and list_label_bak[right] =='S' and price1==0.0 and price2 ==0.0:
                            count = count + 1
                            continue
                        if list_label_bak[left] != list_label_bak[right] and list_label_bak[right] =='S':
                            price1_new = price1_new * BUY_RATE
                            price2_new = price2_new  * PUR_RATE
                            price21 = price2_new  - price1_new
                            rows_buy = [code, list_time_bak, price1_new, biao_cang, price1_time, price2_new,
                                        price2_time, price1, price2, price21, out5, out10]
                            ret_buy['data'].append(rows_buy)
                        elif list_label_bak[left] =='S'  and price1==0.0:#中间出现没有买就该股最后一天的情况，整体往前移
                            n = left
                            num = len_price
                            #整体往前移一个
                            for j in range(n,num-1):
                                list_price_bak[j] = list_price_bak[j+1]
                                list_time_bak[j] = list_time_bak[j+1]
                                list_cang_bak[j] = list_cang_bak[j+1]
                                list_label_bak[j] = list_label_bak[j+1]
                            #print('################', code, list_time_bak[left], list_time_bak[left+1])

                            left = 0 + count * 2
                            price1 = float(list_price_bak[left])
                            price1_time = list_time_bak[left]
                            biao_cang = list_cang_bak[left]
                            biao_cang2 = get_not_ten(biao_cang)
                            price1_new = price1*biao_cang2
                            price2 = float(list_price_bak[right])
                            price2_time = list_time_bak[right]
                            price2_new = float(list_price_bak[right]) * biao_cang2
                            price1_new = price1_new * BUY_RATE
                            price2_new = price2_new  * PUR_RATE
                            if list_label_bak[right]=='S' and list_label_bak[left]=='B':
                                price21 = price2_new - price1_new
                                rows_buy = [code, list_time_bak, price1_new, biao_cang, price1_time, price2_new,
                                            price2_time, price1, price2, price21, out5, out10]
                                ret_buy['data'].append(rows_buy)
                            elif list_label_bak[right]=='B' and list_label_bak[left]=='S':
                                price21 = price1_new - price2_new
                                rows_sell = [code, list_time_bak, price1_new, biao_cang, price1_time, price2_new,
                                             price2_time,
                                             price1, price2, price21, out5, out10]
                                ret_sell['data'].append(rows_sell)
                            else:
                                print('################', code, price1_time, price2_time)
                                print ('ERROR!!!!!!!!!!!!!!')
                        elif list_label_bak[left] != list_label_bak[right] and list_label_bak[right] =='B':
                            price1_new = price1_new * PUR_RATE
                            price2_new = price2_new * BUY_RATE
                            price21 =  price1_new - price2_new
                            rows_sell = [code, list_time_bak, price1_new, biao_cang, price1_time, price2_new, price2_time,
                                         price1, price2, price21, out5, out10]
                            ret_sell['data'].append(rows_sell)
                        ####新增数据
                        if  list_label_bak[left] == 'B' and list_label_bak[right] =='B' and list_label_bak[right+1] =='S':
                            pass
                        count = count + 1


    ###
    ###
    #####  删除一行都是卖出信号的记录
    for i in range(len(ret_buy['data'])):
        price2_new = ret_buy['data'][i][5]
        price2 = ret_buy['data'][i][8]
        price1_new = ret_buy['data'][i][2]
        price1 = ret_buy['data'][i][7]

        if (ret_buy['data'][i][6][-1]== 'S' and price2_new ==0.0 and price2==0.0) or (ret_buy['data'][i][4][-1]== 'S' and price1_new ==0.0 and price1==0.0):
            ret_buy['data'][i] = 'C'
    while 'A' in ret_buy['data']:
        ret_buy['data'].remove('A')
    while 'C' in ret_buy['data']:
        ret_buy['data'].remove('C')
    ret_buy['data'] = addLabel(ret_buy['data'])


    ###
    ###
    #####  找出特殊的记录
    count = 0
    for i in range(len(ret_buy['data'])):
        price1_time = ret_buy['data'][i][4]
        price2_time = ret_buy['data'][i][6]
        #print('################', ret2['data'][i][0], price1_time, price2_time)
        if price1_time[-1] == price2_time[-1]:
            print ('################',ret_buy['data'][i][0],price1_time,price2_time)
            count = count +1
    print ('error sum',count)
    #print (ret2['data'])



    ###
    ###
    #####  删除一行都是卖出信号的记录
    for i in range(len(ret_sell['data'])):
        price2_new = ret_sell['data'][i][5]
        price2 = ret_sell['data'][i][8]
        price1_new = ret_sell['data'][i][2]
        price1 = ret_sell['data'][i][7]

        if (ret_sell['data'][i][6][-1] == 'S' and price2_new == 0.0 and price2 == 0.0) or (
                            ret_sell['data'][i][4][-1] == 'S' and price1_new == 0.0 and price1 == 0.0):
            ret_sell['data'][i] = 'C'
    while 'A' in ret_sell['data']:
        ret_sell['data'].remove('A')
    while 'C' in ret_sell['data']:
        ret_sell['data'].remove('C')
    ret_sell['data'] = addLabel(ret_sell['data'])

    ###
    ###
    #####  找出特殊的记录
    count = 0
    for i in range(len(ret_sell['data'])):
        price1_time = ret_sell['data'][i][4]
        price2_time = ret_sell['data'][i][6]
        # print('################', ret2['data'][i][0], price1_time, price2_time)
        if price1_time[-1] == price2_time[-1]:
            print('################', ret_sell['data'][i][0], price1_time, price2_time)
            count = count + 1
    print('error sum', count)
    # print (ret2['data'])

    df_buy = pd.DataFrame(ret_buy['data'])
    df_buy.columns = [header]


    df_sell = pd.DataFrame(ret_sell['data'])
    df_sell.columns = [header]




    dff1 = df_writer.append(df_buy,ignore_index=True)
    dff2 = df_writer.append(df_sell, ignore_index=True)
    today = time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time()))
    writer = pd.ExcelWriter('../output/{}老B1+老B2-4天fromDtoM_detail_拆分明细盈利.xlsx'.format(today))# 新B1+新B2-4天
    dff1.to_excel(writer, 'B-S')
    dff2.to_excel(writer, 'S-B')
    writer.save()


####
####间隔超过5天或10天的数据增加label
def addLabel(data):
    sum = 0
    for i in range(len(data)):
        price1_time = data[i][4][0:-1]
        price2_time = data[i][6][0:-1]
        #####
        price1_day = datetime.datetime.strptime(price1_time, '%Y-%m-%d %H:%M:%S')
        price2_day = datetime.datetime.strptime(price2_time,'%Y-%m-%d %H:%M:%S')
        days = abs((price1_day - price2_day).days)
        if days > 10:
            data[i][11] = days
            sum += data[i][9]
        elif  days > 5:
            data[i][10] = days
            sum += data[i][9]
    print ('特殊数据的总亏损',sum)
    return data





if __name__ == "__main__":
    logging.basicConfig(
        format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    # filpath = '../input/0302_老B1+老B2_4天_fromDtoM_明细.xlsx'
    # getExcel(filpath)
    filepathes = '../pkl/2018-03-02093658老B1+老B2-4天fromDtoM_detail.pkl'#老B1+老B2-4天fromDtoM_detail2018-02-28095304
    getDetail(filepathes)
    #getExcel()
    #getDetail()
    print(get_not_ten(112400))
