import xlrd
import sys
import os
import tmp_pickle
import csv
import time
import pandas as pd
import glob
import xlrd


#####处理分时源数据  0305 by  gxj   3000多个生成3000个pkl

def getTheFile(filename, this_file=__file__):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(this_file)), filename))

def getFiles(path):
    files= os.listdir(path) #得到文件夹下的所有文件名称
    for file in files: #遍历文件夹
        print(file) #打印结果

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        print(child) # .decode('gbk')是解决中文显示乱码问题

# 读取文件内容并打印
def readFile(filename):
    fopen = open(filename, 'r') # r 代表read
    for eachLine in fopen:
        print ('e')
        #print "读取到得内容如下：",eachLine
    fopen.close()

global dicts
dicts = {}
def GetFileLists(dir, fileList):

    newDir = dir
    if os.path.isfile(dir):
        print(dicts, dicts.keys())
        if dir[-10:] not in dicts:
            dicts[dir[-10:]] = [dir]
            #print('file', dir[-10:], dicts)
        elif dir[-10:] in dicts:
            dicts[dir[-10:]].append(dir)
            print('file',dicts)
        #fileList.append(dir)
    elif os.path.isdir(dir):
        #print ('dir',os.listdir(dir))
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            #print('*****************',dir)
            #newDir = os.path.join(dir, s)
            newDir = dir + '/'+s
            if os.path.isfile(newDir):
                print(dicts, dicts.keys())
                if newDir[-10:] not in dicts:
                    dicts[newDir[-10:]] = [newDir]
                    # print('file', dir[-10:], dicts)
                elif newDir[-10:] in dicts:
                    dicts[newDir[-10:]].append(newDir)
                    print('file', dicts)
            else:
                for s in os.listdir(newDir):
                    newDir = dir + '/' + s

    print ('echo dir$$$$$$$$$$$$$$$$',dicts)
    print('echo dir$$$$$$$$$$$$$$$$', len(dicts))
    #tmp_pickle.wpicke('../pkl_test/' + dicts + '.pkl', dicts)
    return dicts


# def get_dict(dir,dicts,sh_sz):
#     i = 0
#     #if dir[-11]=='/':
#     if len(dir) == 10:
#         #i = i+1
#         key_name = dir[-10:-4] + '.'+ sh_sz +'.csv'
#         print ('key_name',key_name)
#         if key_name not in dicts:
#             dicts[key_name] = [dir]
#             # print('file', dir[-10:], dicts)
#         elif key_name in dicts:
#             dicts[key_name].append(dir)
#             #print('file', dicts)

def get_dict(dir, dicts, sh_sz):
    i = 0
    if dir[-11]=='/':
        # i = i+1
        key_name = dir[-10:-4] + '.' + sh_sz + '.csv'
        print('key_name', key_name)
        if key_name not in dicts:
            dicts[key_name] = [dir]
            # print('file', dir[-10:], dicts)
        elif key_name in dicts:
            dicts[key_name].append(dir)
            # print('file', dicts)

# def GetFileList(dir, fileList):
#     if os.path.isdir(dir):
#         for sh_sz in os.listdir(dir):
#             newDir = dir + '/'
#             if os.path.isdir(newDir):
#                 for s in os.listdir(newDir):
#                     oldDir = newDir + '/' + s
#                     code_list = os.listdir(oldDir)
#                     for i in range(len(code_list)):
#                         dirs = oldDir + '/'+code_list[i]
#                         print (dirs)
#                         if os.path.isfile(dirs):
#                             get_dict(dirs,dicts,sh_sz[:2])
#                             print ('%%%%%%%%%%%',sh_sz[:2])
#                             #dirs = oldDir + '/' + code_list[i][:5] + sh_sz + '.csv'
#     print('echo dir$$$$$$$$$$$$$$$$', dicts)
#     print('echo dir$$$$$$$$$$$$$$$$', len(dicts))
#     tmp_pickle.wpicke('../pkl_test/dicts.pkl', dicts)
#     return dicts

def GetFileList(dir, fileList):
    dicts = {}
    if os.path.isdir(dir):
        for sh_sz in os.listdir(dir):
            newDir = dir + '/'
            if os.path.isdir(newDir):
                for s in os.listdir(newDir):
                    oldDir = newDir  + s
                    code_list = os.listdir(oldDir)
                    for i in range(len(code_list)):
                        dirs_list = os.listdir(oldDir + '/' + code_list[i])
                        print ('111',len(dirs_list))
                        for j in range(len(dirs_list)):
                            dirs = oldDir + '/' + code_list[i] + '/'+dirs_list[j]
                            print('222',dirs)
                            if os.path.isfile(dirs):
                                get_dict(dirs,dicts,s[:2])
                                print ('code是',s[:2])
                                #dirs = oldDir + '/' + code_list[i][:5] + sh_sz + '.csv'
    print('echo dir$$$$$$$$$$$$$$$$', dicts.keys())
    print('echo dir$$$$$$$$$$$$$$$$', len(dicts))
    tmp_pickle.wpicke('../pkl_test/dicts_ticks.pkl', dicts)
    return dicts


if __name__ == "__main__":
    # dff = pd.DataFrame()
    # path = "D:/补充数据"
    # dicts  = {}
    # dicts = GetFileList(path,[])


    dicts = tmp_pickle.rpicke('../pkl_test/dicts_ticks.pkl')
    file_len = len(dicts)
    print ('______________________________长度',file_len,dicts)


    for code,paths in dicts.items():
        #if code=='000300.SH.csv':
            num_len =  len(paths)
            dff = pd.DataFrame()
            dff1 = pd.DataFrame()

            for i in range(num_len):
                if num_len>0:
                    print('CODE',code)
                    print (paths[i])
                    pwd = os.getcwd()
                    os.chdir(os.path.dirname(paths[i]))
                    df = pd.read_csv(os.path.basename(paths[i]),encoding='gbk')
                    os.chdir(pwd)
                    #df = pd.read_csv(paths[i],engine=python)
                    print(len(df))
                    dff = dff.append(df)
                    #print(len(dff))
            print (len(dff))
            dff.to_csv("../fenshi_csv_test/"+code, index=False)














