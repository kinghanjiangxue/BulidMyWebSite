from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论 处理以及回复
    path('post-comment/<int:article_pk>', views.post_comment, name='post_comment'),
    # 处理二级回复
    path('post-comment/<int:article_pk>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]