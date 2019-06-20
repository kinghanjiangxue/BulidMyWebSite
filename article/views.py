
# 引入redirect重定向的模块
from django.shortcuts import render, redirect
from .models import ArticlePost
import markdown
from django.http import HttpResponse
# 引入定义的from表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


# 文章列表
def article_list(request):

    # 取出所有的博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数，载入模板并返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, pk):
    # 取出所有文章
    article = ArticlePost.objects.get(pk=pk)

    # 将Markdown语法渲染成HTML的样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含缩写，表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)

            # 指定数据库中id=1的用户作为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并出入此用户的id
            new_article.author = User.objects.get(id=1)
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
def article_delete(request, pk):
    # 根据对应的id去删除对应的文章
    article = ArticlePost.objects.get(pk=pk)
    # 调用。delete()方法
    article.delete()
    return redirect('article:article_list')
