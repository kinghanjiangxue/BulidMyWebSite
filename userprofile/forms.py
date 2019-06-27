
# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User
from .models import Profile


# 登录时候继承了forms.Form表单类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册表单用户
class UserRegisterForm(forms.ModelForm):

    # 赋值User密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次的输入密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试')


# 扩展字段
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
