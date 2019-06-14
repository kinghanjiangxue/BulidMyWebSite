Django-REST-framework使用技巧(一)

* [1.环境搭建](#1)



<h1 id='1'></h1>

# 1、环境搭建

## 环境
> Python 3.7.2
> 
> MacOS High Sierra
> 
> django-2.2.1 
> 
> djangorestframework-3.9.4

<h3 id = '1.1'></h3>

## 1.1 项目创建


#### 创建目录

	mkdir myblog
	cd myblog


#### 安装虚拟环境 
	
	sudo pip install virtualenv

#### 创建virtualenv，环境隔离我们本地的依赖包关系

	virtualenv env # 会得到下面结果回应
	
```
	Using base prefix '/usr/local/Cellar/python/3.7.2_2/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/administrator/Desktop/Django-REST-Framework/tutorial/env/bin/python3.7
Also creating executable in /Users/administrator/Desktop/Django-REST-Framework/tutorial/env/bin/python
Installing setuptools, pip, wheel...
done.

```
	source env/bin/activate #激活虚拟环境，可以看到以下结果显示
	(env) AdministratordeiMac:tutorial administrator$ 


#### 在虚拟环境安装Django
	
	pip install --upgrade pip #先升级pip
	pip install django # 安装django
	
创建项目，并建立一个app

	django-admin startproject tutorial . #建立Django项目。后面"."表示在当前文件夹建立项目
	python manage.py startapp quickstart 或则django-admin.py startapp quickstart #新建一个APP

