
# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User


# 登录时候继承了forms.Form表单类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
