import re
import sqlite3
import word2wec_method

# 此段代码计算原来数据库中的文书向量并存入，之后无需调用

# 创建与数据库的连接
connection = sqlite3.connect('../database.db')
# 创建一个游标
cur = connection.cursor()

for i in range(1,207):

    cur.execute('select content from rawWrit where id = {};'.format(i))
    text = cur.fetchone()[0]

    if "???" in text or not "本院认为" in text or not "本判决" in text:
        #如果是乱码文件或者不是判决书的形式，则跳过
        pass
    else:
        v = word2wec_method.returnV(text)
        #将计算出的向量(字符串形式)写进数据库
        cur.execute("update rawWrit set v = '%s' where id = '%d';" % (v,i))
        #提交命令
        connection.commit()

#关闭连接
cur.close()
connection.close()
print("保存"
      ""
      ""
      ""
      ""
      "成功！")