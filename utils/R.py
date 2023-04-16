# @Time : 2023/3/16 12:56 
# @Author : 赵浩栋
# @File : R.py 
# @Software: PyCharm
# 定义xhr统一格式
import http

from django.http import JsonResponse, HttpResponse


# 定义统一的json字符串返回
def result(code=200, msg="success", kwargs=None):
    # if data is None:
    #     json_dict = {"code": code, "msg": msg}
    # else:
    #     json_dict = {"code": code, "msg": msg, "data": data}
    json_dict = {"code": code, "msg": msg}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False}, )
