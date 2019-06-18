from django.shortcuts import render
from .models import ArticlePost


def article_list(request):

    # 取出所有的博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数，载入模板并返回context对象
    return render(request, 'article/list.html', context)

