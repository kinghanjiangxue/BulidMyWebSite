
from django.urls import path
from . import views


app_name = 'userprofile'


urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),
]