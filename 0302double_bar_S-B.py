import os
import xlrd
from pylab import *
import time
import datetime
import pandas as pd
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

set_start_per = 0
set_end_per = 0.1


set_start_per_f = -0.12
set_end_per_f = 0

######最高盈利/买入价的主要分布情况

######0301 by gxj 正负盈利的分布柱状图  两条对比
def getTheFile(filename, this_file=__file__):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))


def autolabel(rects, Num=1.12, rotation1=90, NN=1):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() - 0.04 + rect.get_width() / 2., Num * height, '%s' % float(height * NN),
                 rotation=rotation1)


def image_bar(filepath):
    filename = getTheFile(filepath)
    data = xlrd.open_workbook(filename)
    x = []
    x_list = []

    for i in range(1):
        table = data.sheets()[i]
        row_len = table.nrows
        for j in range(1,row_len):
            rows = table.row_values(j)
            x.append(rows[10])
    print ('len(x)',len(x))
    x = np.array(x)

    x_min = -0.12
    x_max = 0.12
    print (x_min)
    print (x_max)
    while x_min <= x_max:
        x_list.append(x_min)
        x_min = x_min + 0.01
    print (x_list)
    print(len(x_list))


    x_num = []
    x_len = len(x_list) - 1
    for j in range(x_len):
        num = ((x > x_list[j]) & (x <= x_list[j + 1])).sum()
        #if x_list[j]>0.11 and x_list[j + 1]<=0.12:
        print ('AAAA',x_list[j],num)
        x_num.append(num)
    x_num.append(-0)
    print('*****')
    print(x_num)
    print(len(x_num))



    # x_list2 = ['-109%~-99%','-99%~-89%', '-89%~-79%', '-79%~-69', '-69%~-59%','-59%~-49%',
    #        '-49%~-39%', '-39%~-29%','-29%~-19%','-19%~-9%','-9%~1%','1%~11%',
    #        '11%~21%', '21%~31%','31%~41%','41%~51%','51%~61%','61%~69%']

    # x_list2 = ['-11%~-10%','-10%~-9%', '-9%~-8%', '-8%~-7%', '-7%~-6%','-6%~-5%', '-5%~-4%', '-4%~-3%',
    #            '-3%~-2%', '-2%~-1%','-1%~0%','0%~-1%', '1%~2%', '2%~3%', '3%~4%','4%~5%', '5%~6%', '6%~7%',
    #            '7%~8%', '8%~9%', '9%~10%']

    ########区间段生成excel
    z_min = -0.08
    z_max = 0.25
    # z_min = x.min()
    # z_max = x.max()
    print ('aaaaaaaaaaa',z_min)
    print ('bbbbbbbbbb',z_max)
    z_list = []
    z_num_per = []

    while z_min <= z_max:
        z_list.append(z_min)
        z_min = z_min + 0.01

    '''额外增加比例个数生成excel文件 start
    z_num = []
    z_len = len(z_list) - 1
    for p in range(z_len):
        num = ((x > z_list[p]) & (x <= z_list[p + 1])).sum()
        z_num.append(num)
        z_num_per.append('{:%}'.format((z_list[p]))+'~~~~'+'{:%}'.format((z_list[p+1])))
        if num>2:
            print ('序号',p)
    #z_num.append(-0)
    print ('*****************************************start')
    print(z_min)
    print(z_max)
    #print(z_list[33])

    print(len(z_list))
    print(z_num)
    #print (z_num[415:])
    print(len(z_num))
    #print(z_num_per[33])

    print(len(z_num_per))

    df_writer = pd.DataFrame()
    df_tmp = pd.DataFrame(np.array(z_num_per).T,np.array(z_num).T)
    print (df_tmp)
    #df_tmp2 = pd.DataFrame(np.array(z_num[415:]).T)
    #df_tmp.columns = ['百分比','占比数']
    df_writer = df_writer.append(df_tmp)
    #df_writer = df_writer.append(df_tmp2, ignore_index=True)
    today = time.strftime('%Y-%m-%d%H%M%S', time.localtime(time.time()))
    writer = pd.ExcelWriter('../output/占比{}.xlsx'.format(today))
    df_writer.to_excel(writer, 'Sheet1')
    writer.save()
    print('*****************************************end')
    额外增加比例个数生成excel文件 end'''


    x_list2 = ['-12%~-11%','-11%~-10%', '-10%~-9%', '-9%~-8%', '-8%~-7%', '-7%~-6%', '-6%~-5%', '-5%~-4%', '-4%~-3%',
               '-3%~-2%', '-2%~-1%', '-1%~0%', '0%~1%', '1%~2%', '2%~3%', '3%~4%', '4%~5%', '5%~6%', '6%~7%',
               '7%~8%', '8%~9%', '9%~10%','10%~11%','11%~12%','12%~MAX']
    print(len(x_list2))
    print ('&&&&&&&&&')

    rects = plt.bar(x_list, x_num, width=0.003, align='center')
    plt.xlim(x_min, x_max)
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            # print(height)
            # height = float(height / 5081) *100
            # print(height)
            # height = round(height, 2)
            # print (height)
            # plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % height)
            plt.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, '%d' % height)

    autolabel(rects)
    plt.xticks(x_list, x_list2, rotation=0)
    plt.gca().invert_xaxis()
    plt.title(u'(最高盈利)/(买入价)'+filepath[14:17])
    plt.xlabel(u'百分比')
    plt.ylabel(u'占比数')
    plt.show()


def autolabel2(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%d' % float(height))
def get_time_per(filepath):
    filename = getTheFile(filepath)
    data = xlrd.open_workbook(filename)
    x = []
    x_list = []
    y = []
    y_list = []
    x_num_list = []  #正

    x_period_list = []
    x_tick_list = []
    for i in range(1):
        table = data.sheets()[i]
        row_len = table.nrows
        for j in range(1, row_len):
            rows = table.row_values(j)
            if rows[10]>=set_start_per and rows[10]<set_end_per and i == 0:
                x.append(rows[4])
                x_list.append(rows[4][0:10])
            if rows[10]>=set_start_per and rows[10]<set_end_per and i == 1:
                x.append(rows[6])
                x_list.append(rows[6][0:10])
            if rows[10]>=set_start_per_f and rows[10]<set_end_per_f and i == 0:
                y.append(rows[4])
                y_list.append(rows[4][0:10])
            if rows[10]>=set_start_per_f and rows[10]<set_end_per_f and i == 1:
                y.append(rows[6])
                y_list.append(rows[6][0:10])
    x_list = sort(x_list)
    y_list = sort(y_list)
    print (x)
    print (x_list)
    print (len(x))


    first_day = x_list[0]
    i = 0
    while first_day<=x_list[-1]:
        first_day = datetime.datetime.strptime(first_day,'%Y-%m-%d')
        delta = datetime.timedelta(days=30)
        second_day = (first_day + delta).strftime('%Y-%m-%d')
        first_day = first_day.strftime('%Y-%m-%d')
        num = ((x_list > first_day) & (x_list <= second_day)).sum()
        x_num_list.append(num)
        x_period_list.append(first_day+'---'+second_day)
        x_tick_list.append(i)
        first_day = second_day
        i = i+1

    print (x_num_list)
    print(x_period_list)
    print(len(x_num_list))
    print(len(x_period_list))

    y_num_list = []  # 负
    y_period_list = []
    first_day_f = x_list[0]
    f = 0
    while first_day_f <= x_list[-1]:
        first_day_f = datetime.datetime.strptime(first_day_f, '%Y-%m-%d')
        delta = datetime.timedelta(days=30)
        second_day_f = (first_day_f + delta).strftime('%Y-%m-%d')
        first_day_f = first_day_f.strftime('%Y-%m-%d')
        num_f = ((y_list > first_day_f) & (y_list <= second_day_f)).sum()
        y_num_list.append(num_f)
        y_period_list.append(first_day_f + '---' + second_day_f)
        first_day_f = second_day_f
        f = f + 1
    print ('***********************')
    print(y)
    print(y_list)
    print(len(y))
    print(y_num_list)
    print(y_period_list)
    print(len(y_num_list))
    print(len(y_period_list))
    total_width, n = 0.8, 2
    wid = total_width / n
    rects = plt.bar(x_tick_list,x_num_list,width=wid,label='正盈利占比数',fc='r')
    for i in range(len(x_tick_list)):
        x_tick_list[i] = x_tick_list[i] + wid
    rects_b = plt.bar(x_tick_list,y_num_list,width=wid,label='负盈利占比数',fc='g')





    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width(), 1.03 * height, '%d' % height)
    autolabel2(rects)
    autolabel2(rects_b)
    plt.xticks(x_tick_list,x_period_list, rotation=90)
    # plt.xticks(x_tick_list, y_period_list, rotation=90)
    #plt.gca().invert_xaxis()
    plt.title(u'(最高盈利)/(卖出价)'+filepath[14:17])
    plt.xlabel(u'时间段')
    plt.ylabel(u'占比数')
    plt.legend(loc='upper left')
    plt.show()
    # m = x_list[0]
    # for j in range(1,len(x_list)):
    #     if
    ####日期的每天的加减  strptime(string,[, format]) 根据指定的格式把一个时间字符串解析为时间元组。








filepath = '../output/0306B-S.xlsx'
#image_bar(filepath)
get_time_per(filepath)