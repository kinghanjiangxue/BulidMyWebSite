from django.test import TestCase
import datetime
from django.utils import timezone
from article.models import ArticlePost
from django.contrib.auth.models import User
from django.urls import reverse
from time import sleep


class ArticlePostModelTests(TestCase):
    def test_was_created_recently_with_future_articel(self):
        # 如果文章创建时间为未来，则返回FALSE
        author = User(username='user', password='test_password')
        author.save()

        future_article = ArticlePost(
            author=author,
            title='test',
            body='test',
            created_time=timezone.now() + datetime.timedelta(days=30)
        )

        self.assertIs(future_article.was_created_recently(), False)

    def test_was_created_recently_with_seconds_before_article(self):
        # 若文章创建时间为1分钟内，则返回TRUR
        author = User(username='user1',password='test_password')
        author.save()
        seconds_before_article = ArticlePost(
            author=author,
            title='test1',
            body='test1',
            created_time=timezone.now() - datetime.timedelta(seconds=45)
        )

        self.assertIs(seconds_before_article.was_created_recently(), True)

    def test_was_created_recently_with_hours_before_article(self):
        # 如果文章创建为几个小时前，则返回FALSE
        author = User(username='test2', password='twst_password')
        author.save()
        hours_before_article = ArticlePost(
            author=author,
            title='test2',
            body ='test2',
            created_time=timezone.now() - datetime.timedelta(hours=3)
        )

        self.assertIs(hours_before_article.was_created_recently(), False)

    def test_was_created_recently_with_days_before_article(self):
        # 如果文章创建为几个小时前，返回FALSE'
        author = User(username='user2', password='test_password')
        author.save()
        months_before_article = ArticlePost(
            author=author,
            title='test3',
            body='test3',
            created_time=timezone.now() - datetime.timedelta(days=5)
        )
        self.assertIs(months_before_article.was_created_recently(), False)


class ArticlePostViewTests(TestCase):

    def test_increase_veiws(self):
        # 请求详情视图是偶，阅读量+1
        author = User(username='user4',password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test4',
            body='test4',
        )
        article.save()
        self.assertIs(article.total_views, 0)

        url = reverse('article:article_detail', args=(article.pk,))
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(pk=article.pk)
        self.assertIs(viewed_article.total_views,1)

    def test_increase_views_but_changge_update_field(self):
         # 请求详情视图时候，不改变update 字段
         author = User(username='user5', password='test_password')

         author.save()
         article = ArticlePost(
             author=author,
             title='test5',
             body='test5',
         )
         article.save()

         sleep(0.5)
         url = reverse('article:article_detail', args=(article.pk,))
         response = self.client.get(url)

         viewed_article  =ArticlePost.objects.get(pk=article.pk)
         self.assertIs(viewed_article.update_time - viewed_article.created_time < timezone.timedelta(seconds=0.1), True)





