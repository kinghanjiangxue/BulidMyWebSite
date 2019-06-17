from django.shortcuts import render
# 导入HTTPResponse模块
from django.http import HttpResponse


def article_list(request):
    return HttpResponse('Hello World!')

