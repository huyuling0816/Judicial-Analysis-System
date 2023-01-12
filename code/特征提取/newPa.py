#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import fnmatch
import os
import re
import sqlite3
import zipfile
from win32com import client as wc
from time import sleep
import pyautogui
import pyperclip
import unicodedata as ucd
from word2evc import word2wec_method
from 分词.中文分词.分词算法 import conclude
from 特征提取 import get_data

def getText(filename):
    f = open(filename, encoding='GB18030')
    content = []
    for line in f.readlines():
        temp = ucd.normalize('NFKC', line.strip('\n')).replace(' ', '') # 去掉列表中每一个元素的换行符
        content.append(temp.replace('"',''))  # 去掉双引号
    f.close()
    return ''.join(content)

def unzip (path,newPath):
    #获取目录下所有文件名
    filenames = os.listdir(path)
    for filename in filenames:
        filepath = os.path.join(path,filename)
        # 获取压缩文件
        if(filename.endswith(".zip")):
            zip_file = zipfile.ZipFile(filepath)
            # #获取压缩文件的文件名
            # newfilepath = filename.split(".",1)[0]
            # newfilepath = os.path.join(path,newfilepath)
            # #根据获取的压缩文件的文件名建立相应的文件夹
            # if os.path.isdir(newfilepath):
            #     pass
            # else:
            #     os.mkdir(newfilepath)
            #解压文件
            for name in zip_file.namelist():
                zip_file.extract(name,newPath)
            zip_file.close()
            Conf = os.path.join(newPath,'conf')
            #删除原先压缩包
            if os.path.exists(filepath):
                os.remove(filepath)

def Translate(path):
    '''
    将一个目录下所有doc和docx文件转成txt
    该目录下创建一个新目录newdir
    新目录下fileNames.txt创建一个文本存入所有的word文件名
    本版本具有一定的容错性，即允许对同一文件夹多次操作而不发生冲突
    '''
    # 该目录下所有文件的名字
    global all_FileNum
    files = os.listdir(path)
    # 创建一个文本存入所有的word文件名
    wordapp = wc.Dispatch('Word.Application')
    for filename in files:
        # 如果不是word文件：继续
        if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx'):
            continue
        # 如果是word临时文件：继续
        if fnmatch.fnmatch(filename, '~$*'):
            continue
        docpath = os.path.abspath(os.path.join(path, filename))

        # 得到一个新的文件名,把原文件名的后缀改成txt
        new_txt_name = ''
        if fnmatch.fnmatch(filename, '*.doc'):
            new_txt_name = filename[:-4] + '.txt'
        else:
            new_txt_name = filename[:-5] + '.txt'
        word_to_txt = os.path.join(path, new_txt_name)
        doc = wordapp.Documents.Open(docpath)
        # 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
        doc.SaveAs(word_to_txt, 4)
        doc.Close()
        os.remove(os.path.join(path,filename))

    wordapp.Quit()

def searchTimePro(text):
    if "二〇" in text and "日" in text:
        times = re.findall(r"二〇(.+?)日",text)
        time =""
        for t in times:
            if len(t) <= 11:
                time = t
        time = "二〇" + time + "日"
        year = re.findall(r"二〇(.+?)年",time)[0]
        month = re.findall(r"年(.+?)月",time)[0]
        day = re.findall(r"月(.+?)日",time)[0]
        res = '20'

        if year == "二一":
            res+="21"
        elif year =="二〇":
             res+='20'
        elif year =="一九":
             res+='19'
        elif year =="一八":
             res+='18'
        elif year =="一七":
            res+='17'
        elif year =="一六":
            res+='16'
        elif year =="一五":
            res+='15'
        elif year =="一四":
            res+='14'
        elif year =="一三":
            res+='13'
        elif year =="一二":
            res+='12'
        elif year == "一一":
            res+='11'
        elif year == "一〇":
            res+='10'
        elif year == "〇九":
            res+='09'
        elif year == "〇八":
            res+='08'
        elif year == "〇七":
            res+='07'
        elif year == "〇六":
            res+='06'
        elif year == "〇五":
            res+='05'
        elif year == "〇四":
            res+='04'
        elif year == "〇三":
            res+='03'
        elif year == "〇二":
            res+='02'
        elif year == "〇一":
            res+='01'
        elif year == "〇〇":
            res+='00'

        res+="-"

        if month == "一":
            res+="01"
        elif month == "二":
            res+="02"
        elif month == "三":
            res+="03"
        elif month == "四":
            res+="04"
        elif month == "五":
            res+="05"
        elif month == "六":
            res+="06"
        elif month == "七":
            res+="07"
        elif month == "八":
            res+="08"
        elif month == "九":
            res+="09"
        elif month == "十":
            res+="10"
        elif month == "十一":
            res+="11"
        elif month == "十二":
            res+="12"

        res+="-"

        if day == "一":
            res+="01"
        elif day == "二":
            res+="02"
        elif day == "三":
            res+="03"
        elif day == "四":
            res+="04"
        elif day == "五":
            res+="05"
        elif day == "六":
            res+="06"
        elif day == "七":
            res+="07"
        elif day == "八":
            res+="08"
        elif day == "九":
            res+="09"
        elif day == "十":
            res+="10"
        elif day == "十一":
            res+="11"
        elif day == "十二":
            res+="12"
        elif day == "十三":
            res+="13"
        elif day == "十四":
            res+="14"
        elif day == "十五":
            res+="15"
        elif day == "十六":
            res+="16"
        elif day == "十七":
            res+="17"
        elif day == "十八":
            res+="18"
        elif day == "十九":
            res+="19"
        elif day == "二十":
            res+="20"
        elif day == "二十一":
            res+="21"
        elif day == "二十二":
            res+="22"
        elif day == "二十三":
            res+="23"
        elif day == "二十四":
            res+="24"
        elif day == "二十五":
            res+="25"
        elif day == "二十六":
            res+="26"
        elif day == "二十七":
            res+="27"
        elif day == "二十八":
            res+="28"
        elif day == "二十九":
            res+="29"
        elif day == "三十":
            res+="30"
        elif day == "三十一":
            res+="31"

        return res
    else:
        return 0

def databaseEntry(path,word):
    # 创建与数据库的连接
    connection = sqlite3.connect('../database.db')
    # 创建一个游标
    cur = connection.cursor()
    # 存取内容
    for root, dirs, files in os.walk(path):
        for file in files:
            # 获取文件名
            title = str(file[:-4])
            if len(title) >= 100:
                title = title[0:100]
            # 文件路径
            filepath = os.path.join(path, file)
            content = getText(filepath)
            if len(content) > 30000:
                content = content[0:30000]
            if "???" in content or not "本院认为" in content or not "本判决" in content:
                # 乱码或不符合判决书形式
                pass
            else:
                # 通过正则表达式匹配出文书时间
                time = searchTimePro(content)
                # 得到转化为字符串的向量
                v = word2wec_method.returnV(content)
                # 得到分词结果
                dict1 = conclude.cut(content)
                wordSeg = "{"
                for key, value in dict1.items():
                    wordSeg += "\'%s\':%s" % (key, value)
                    wordSeg += ", "
                wordSeg = wordSeg[:-2] + "}"
                # 得到特征要素
                dict2,pattern = get_data.word_process_text(content)
                characteristic = "{"
                for key, value in dict2.items():
                    characteristic += "\'%s\':%s" % (key, value)
                    characteristic += ", "
                characteristic = characteristic[:-2] + "}"
                # 写入数据库
                cur.execute("INSERT INTO rawWrit VALUES (null,?,?,?,?,?,?,?,?,?,?);",(word,'NULL',title,content,time,v,0,wordSeg,characteristic,'NULL'))
                connection.commit()
    # 关闭连接
    cur.close()
    connection.close()

def fileProcess(path,newPath,word):
    unzip(path,newPath)
    Translate(newPath)
    # 成功存入本地后就可以告诉用户
    print('成功存至本地！')
    # 然后再进行存入数据库的操作，因为计算向量、分词结果和特征要素并存入数据库比较慢
    databaseEntry(newPath,word)
    print('成功存至数据库！')

def download(startTime,endTime,num):
    # 移动到googlechrome并点击
    pyautogui.moveTo(492, 1401, 0.1)
    pyautogui.click()
    # 移动到高级检索并点击
    pyautogui.moveTo(476, 629)
    pyautogui.click()
    # 全文检索、开始日期、结束日期、检索按钮
    pyautogui.moveTo(814, 717, 1)
    pyautogui.click()
    pyperclip.copy(word)
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.moveTo(1357, 973, 0.5)
    sleep(1)
    pyautogui.click()
    pyperclip.copy(startTime)
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.moveTo(1545, 972, 0.5)
    sleep(1)
    pyautogui.click()
    pyperclip.copy(endTime)
    pyautogui.hotkey('ctrl', 'v')

    #选择文书类型
    pyautogui.moveTo(831,963,0.5)
    pyautogui.click()
    pyautogui.moveTo(646,1119,0.5)
    pyautogui.click()

    pyautogui.moveTo(934, 1279, 0.5)
    pyautogui.click()
    sleep(15)

    for i in range(0,num//5):
        #全选
        pyautogui.moveTo(1665,1000,0.5)
        pyautogui.click()
        #批量下载
        pyautogui.moveTo(1980,995,0.5)
        pyautogui.click()
        if not i == num//5-1:
            #下移
            sleep(1)
            pyautogui.scroll(-3000)
            #下一页
            pyautogui.moveTo(1484,977,0.5)
            pyautogui.click()
            sleep(2)
            #上移
            sleep(2)
            pyautogui.scroll(3000)

    #清空搜索条件
    pyautogui.moveTo(1947,805)
    pyautogui.click()

if __name__=="__main__":

    # 传入参数
    word = input("Enter a word:")
    num = int(input("Enter a num:"))
    startTime = input("Enter start time:")
    endTime = input("Enter end time:")
    startTime = startTime.split("T",1)[0]
    endTime = endTime.split("T",1)[0]

    # 创建一个子文件夹用于存放下载数据
    path = 'D:\南京大学0\数据科学大作业相关\爬取文书文件\\'
    filename = os.path.join(path, word + datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(filename)

    # 创建与数据库的连接
    connection = sqlite3.connect('../database.db')
    # 创建一个游标
    cur = connection.cursor()
    cur.execute("select content from rawWrit where searchWord = '{}' and create_date between '{}' and '{}'".format(word,startTime,endTime))
    contents = cur.fetchall()
    cur.execute("select title from rawWrit where searchWord = '{}' and create_date between '{}' and '{}'".format(word,startTime,endTime))
    titles = cur.fetchall()
    length = len(contents)

    # 若数据库中有足够的文书，那么可以直接从数据库中取并保存到本地
    if length>=num:
        for i in range(0,num):
            title = titles[i][0] + '.txt'
            content = contents[i][0]
            thisPath = os.path.join(filename,title)
            file = open(thisPath,'w')
            file.write(content)
    # 数据库中文书数量不足，直接从文书网下载
    else:
        print("数据库中文书数量不足")
        download(startTime,endTime,num)
        # 等待下载
        sleep(15)
        fileProcess('D:\南京大学0\数据科学大作业相关\爬取文书文件',filename,word)
    print("下载成功！")

    cur.close()
    connection.close()

