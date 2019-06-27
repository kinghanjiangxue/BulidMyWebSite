from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required # 验证登录的装饰器
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile

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


# 用户注册

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客页面
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或者POST请求数据')


# 删除用户操作
@login_required(login_url='/userprofile/login/')
def user_delete(request, pk):
    user = User.objects.get(pk=pk)

    # 验证登录用户、待删除用户是否相同
    if request.user == user:
        # 退出登录，删除数据并返回列表
        logout(request)
        user.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('你没有删除操作的权限。')

