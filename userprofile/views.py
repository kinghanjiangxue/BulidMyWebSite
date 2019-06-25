from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():

            # .clear_data 清晰出合法的数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匀匹配则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存到session中，即实现了登录操作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('账号或者密码错误，请重新输入~')
        else:
            return HttpResponse('账号或者密码输入不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('请使用GET或者POST请求数据')


# 用户退出登录
def user_logout(request):
    logout(request)
    return redirect('article:article_list')
