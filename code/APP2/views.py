from django.shortcuts import render
from . import nlp_method
import json
from django.http import JsonResponse
from APP1.views import get_data

# Create your views here.


def fun(request):
    json_dict = json.loads(request.body.decode()).get("0", None)
    text = json_dict.get("text") ;
    jsonDict = nlp_method.cut(text)    #dict
    dict_feature, pattern = get_data.word_process_text(text)
    result_dict = {
        "cut": jsonDict,
        "feature": dict_feature
    }
    return JsonResponse(result_dict)


"""
性别：男
相关法院：【】
"""

