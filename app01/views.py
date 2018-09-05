from django.shortcuts import render,redirect,HttpResponse
from app01 import models


def change_gender(request,id):
    # 获取ajax发送过来的数据
    gender = request.POST.get("gender")
    # 更新到数据库中
    models.Author.objects.filter(pk=id).update(gender=gender)
    return HttpResponse("ok!")
