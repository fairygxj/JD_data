import os
import xlrd
import datetime
from WindPy import w
import pandas as pd
import time
import tushare as ts
import tmp_pickle

def getTheFile(filename, this_file=__file__):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))

#获取工作日
def getWorkDay(header):
    day_list = []
    for i in header:
        t = (datetime.datetime.strptime(i, "%Y/%m/%d"))
        x = 1
        k = 1
        while x == 1:
            t2 = t + datetime.timedelta(days=k)
            b = ts.is_holiday(str(t2)[0:10])
            t2 = t2.strftime("%Y-%m-%d")
            if b == False:
                day_list.append(t2)
                x = 2
            else:
                k += 1
    return day_list

def isWorkDay(monthtime):
    monthtime = datetime.datetime.strptime(monthtime, '%Y-%m-%d')
    x = 1
    k = 1
    while x == 1:
        monthtime = monthtime+ datetime.timedelta(days=k)
        b = ts.is_holiday(str(monthtime)[0:10])
        if b == False:
            x = 2
        else:
            k += 1
    return monthtime





def get_sixcode(code):
    """
    返回一个标准6位的编码 带后缀
    :param code:
    :return:
    """
    code = str(code)
    # 补齐code 并且判断是.SZ  or .SH
    if len(code) == 1 or len(code) == 2 or len(code) == 3 or len(code) == 3 or len(code) == 4 or len(code) == 5:
        code = code.zfill(6)
    if int(code[0]) == 6:
        code = code + ".SH"
    else:
        code = code + ".SZ"
    return code


def add_suffix(lists):
    """
    "给code添加后缀"
    :param lists:
    :return: list
    """
    list1 = map(get_sixcode, lists)
    return list(list1)







def getST():
    w.start()
    filename = getTheFile('../input/新B1+新B2-4天.xlsx')
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    count = 0
    row_data_list = []
    df_data = pd.DataFrame()
    header = table.row_values(0)
    #header2 = getWorkDay(header)
    today = time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))
    #tmp_pickle.wpicke('../pkl/workday{}.pkl'.format(today), header2)
    header2 = tmp_pickle.rpicke('../pkl/workday2018-02-01102624.pkl')
    print('header', len(header))
    print ('header2',len(header2))

    for i in range(ncols):#ncols
        col_data = []
        code_list = []
        for j in range(1,nrows):#nrows
            ####获取股票池的股票代码
            code = table.row_values(j)[i]
            code_suf = get_sixcode(int(code))
            code_list.append(code_suf)
            ###获取股票池日期 并设定开始结束时间


        '''
        标记收盘涨停或跌停状态, 
        1表示涨停；-1则表示跌停；0表示未涨跌停。   
        涨跌停状态
        '''
        date_time = table.row_values(0)[i]
        date_time = (datetime.datetime.strptime(date_time, '%Y/%m/%d'))
        print('startstart', date_time)
        month_time = str(date_time + datetime.timedelta(days=40))[0:10]


        month_time = (datetime.datetime.strptime(month_time, '%Y-%m-%d')).strftime('%Y-%m-%d')[0:10]
        print('endendend', month_time)
        month_time = isWorkDay(month_time)
        print('endendend', month_time)

        date_time = str(date_time)[0:10]
        month_time = str(month_time)[0:10]


        work_day = header2[i]
        open_list = w.wsd(code_list, "open", date_time, date_time,'PriceAdj=F').Data[0]
        close_list = w.wsd(code_list, "close", month_time, month_time,'PriceAdj=F').Data[0]
        industry_list = w.wsd(code_list, "industryname", date_time, date_time,
              "bondPriceType=2;industryType=1;industryStandard=1;Days=Weekdays").Data[0]
        state_list = w.wsd(code_list,"maxupordown",date_time,date_time, "").Data[0]
        state2_list = w.wsd(code_list,"maxupordown",work_day,work_day, "").Data[0]


        ###截止指定日期，指定证券连续停牌天数（包括指定日）。
        ###其中：
        ###1、暂停上市股份在暂停上市期间，该指标返回为空。
        ###2、该指标仅适用沪深股票,当指定日期为市场非交易日时，前推至最近市场交易日。
        ting_list = w.wsd(code_list, "susp_days",date_time,date_time, "bondPriceType=2").Data[0]
        state_len =len(state_list)
        ting_len = len(ting_list)
        code_len = len(code_list)
        state2_len = len(state2_list)
        #up_len = len(upordown_list)
        ting_len = len(ting_list)
        if state2_len!=state_len!= ting_len:
            print ('ERROR')

        header = []
        header.append(date_time+'--'+month_time)
        header.append('所属板块（申万）')
        header.append('涨跌停状态')
        header.append('T+1涨跌停状态')
        header.append('月涨跌幅')#30%
        header.append('停牌股票天数')
        col_data.append(header)
        for m in range(state_len):
            row_data = []
            code = code_list[m]
            industry = industry_list[m]
            state = state_list[m]
            state2 = state2_list[m]
            tingup = (close_list[m] - open_list[m])/open_list[m] *100
            if tingup >0 and tingup <30:
                tingup = 1 #涨了
            elif tingup<0 and tingup >-30:
                tingup = -1  # 跌了
            else:
                tingup = "%.2f%%" % tingup
            print('open_list[m]', open_list[m])
            print ('close_list[m]',close_list[m])
            print('tingup', tingup)
            ting = ting_list[m]
            row_data.append(code)
            row_data.append(industry)#所属板块
            row_data.append(state)
            row_data.append(state2)##涨跌停状态
            row_data.append(tingup) ##月涨跌幅
            row_data.append(ting)
            count = count +1
            print ('############count',count,date_time,month_time,code)
            col_data.append(row_data)
        print ('col_data',col_data)
        df_clo = pd.DataFrame(col_data)
        if len(df_data)> 0:
            df_data = pd.concat([df_data,df_clo],axis=1)
        else:
            df_data = pd.DataFrame(col_data)
        print('df_data', df_data)
    today = time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))
    writer = pd.ExcelWriter('../output/新B1+新B2-4天-upOrdown{}.xlsx'.format(today))
    df_data.to_excel(writer, 'Sheet1')
    writer.save()


getST()