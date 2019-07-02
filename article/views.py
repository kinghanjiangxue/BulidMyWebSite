
# 引入redirect重定向的模块
from django.shortcuts import render, redirect
from .models import ArticlePost
import markdown
from django.http import HttpResponse
# 引入定义的from表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


# 文章列表
def article_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用Q对象进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将search参数置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示1篇文章
    paginator = Paginator(article_list, 3)

    # 获取url中的页面
    page = request.GET.get('page')

    # 将导航栏对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order, 'search': search}
    # render函数，载入模板并返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, pk):
    # 取出所有文章
    article = ArticlePost.objects.get(pk=pk)

    # 浏览量+ 1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将Markdown语法渲染成HTML的样式
    md = markdown.Markdown(
        extensions=[
            # 包含缩写，表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)

            # 此时请重新创建用户，并出入此用户的id
            new_article.author = User.objects.get(id=request.user.pk)
            # 将文章保存到数据库中
            new_article.save()

            # 完成后返回文章列表
            return redirect('article:article_list')
        else:
            return HttpResponse('内容填写有误，请重新填写啦。')
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, pk):
    # 根据对应的id去删除对应的文章
    article = ArticlePost.objects.get(pk=pk)
    # 过滤费作者用户
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章')
    else:
        # 调用。delete()方法
        article.delete()
        return redirect('article:article_list')


# 编辑文章
@login_required(login_url='userprofile/login/')
def article_update(request, pk):

    """
    更新文章的视图函数
    通过POST方法提交表单，更新title，body字段
    GET方法进入初始化表单页面
    PK：文章的id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(pk=pk)

    # 过滤费作者用户
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章')
    else:

        # 判断用户是否为POST表单提交数据
        if request.method == 'POST':
            # 将提交数据赋值到表单实例中
            article_post_form = ArticlePostForm(data=request.POST)
            # 判断提交的数据是否满足模型要求
            if article_post_form.is_valid():
                # 保存新写入的title，body数据并保存
                article.title = request.POST['title']
                article.body = request.POST['body']
                article.save()
                # 完成之后返回到修改后的文章中，需要传入文章的id值
                return redirect('article:article_detail', pk=pk)
            # 如果不合法，返回错误信息
            else:
                return HttpResponse('表单数据内容有误，请重新填写。')

        # 如果用户是GET请求获取数据
        else:

            # 创建表单实例
            article_post_form = ArticlePostForm()
            # 赋值上下文。将article文章对象也传递进去，以便提取旧的内容
            context = {'article': article, 'article_post_form':article_post_form}
            # 将响应返回到模板中去
            return render(request, 'article/update.html', context)

