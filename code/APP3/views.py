from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
import os

# Create your views here.


def fun(request):
    json_dict = json.loads(request.body.decode()).get("0", None)
    title_temp = json_dict.get("title")
    title = os.path.split(str(title_temp))[1].split(".txt")[0]   # 不带全路径和尾缀的标题
    name = json_dict.get("name")
    gender = json_dict.get("gender")
    nationality = json_dict.get("nationality")
    birthplace = json_dict.get("birthplace")
    crime = json_dict.get("crime")
    court = json_dict.get("court")
    extra = json_dict.get("extra")
    accident = json_dict.get("accident")
    guilt = json_dict.get("guilt")
    blame = json_dict.get("blame")
    reduce = json_dict.get("reduce")
    add = json_dict.get("add")
    result = json_dict.get("result")
    path = "D:\\数据科学爬取案件\\案件标注文件夹\\"+title+".json"
    label_dict = {"当事人": name, "性别": gender, "民族": nationality, "出生地": birthplace, "罪名": crime, "相关法院": court, "补充": extra
    }
    feature_dict = {
        "事故类型": accident,
        "罪名": guilt,
        "主次责任": blame,
        "减刑因素": reduce,
        "加刑因素": add,
        "判决结果": result
    }
    with open(path, "w") as f:     # write打开方式，清空写入
        f.write("分词标注：")
        json.dump(label_dict, f, ensure_ascii=False)
        f.write("\n特征要素：")
        json.dump(feature_dict, f, ensure_ascii=False)
    return JsonResponse({"path": path})

