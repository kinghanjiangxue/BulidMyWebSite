from django.shortcuts import render
from .models import ArticlePost
import markdown


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
