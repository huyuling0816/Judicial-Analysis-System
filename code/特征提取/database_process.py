# -*- coding:utf-8 -*-

import re
import sqlite3
# import word2wec_method
from 特征提取 import get_data
def searchTimePro(text):
    if "二〇" in text and "日" in text:
        times = re.findall(r"二〇(.+?)日",text)
        time =""
        for t in times:
            if len(t)<=11:
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

def searchTime(text):
    if "二〇" in text and "日" in text:
        times = re.findall(r"二〇(.+?)日",text)
        time =""
        for t in times:
            if len(t)<=11:
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

        return int(res)
    else:
        return 0

# 创建与数据库的连接
connection = sqlite3.connect('../database.db')
# 创建一个游标
cur = connection.cursor()

cur.execute("select content from rawWrit where searchWord = '盗窃'")
text = cur.fetchall()

for content in text:

    time = searchTimePro(content[0])

    # SQL查询语句
    dict,pattern = get_data.word_process_text(content[0])

    # 将得到的字典转化为字符串（字符串转化为字典用eval（str））
    str = "{"
    for key, value in dict.items():
        str += "\'%s\':%s" % (key, value)
        str += ", "
    str = str[:-2] + "}"

    print(str)

    SQL = "update rawWrit set characteristicElement = ? where content = ?;"
    arg = (str,content[0])
    # 执行SQL语句
    cur.execute(SQL, arg)
    connection.commit()

# 增加两列
# cur.execute('alter table rawWrit add time int(30000000);')
# cur.execute('alter table rawWrit add characteristicElement  char(10000);')
# connection.commit()

# 计算原来数据库中的文书向量并存入
# for i in range(1,207):
#
#     cur.execute('select content from rawWrit where id = {};'.format(i))
#     text = cur.fetchone()[0]
#
#     if "???" in text or not "本院认为" in text or not "本判决" in text:
#         #如果是乱码文件或者不是判决书的形式，则跳过
#         pass
#     else:
#         v = word2wec_method.returnV(text)
#         #将计算出的向量(字符串形式)写进数据库
#         cur.execute("update rawWrit set v = '%s' where id = '%d';" % (v,i))
#         #提交命令
#         connection.commit()

# 关闭连接
cur.close()
connection.close()
# print("保存成功！")