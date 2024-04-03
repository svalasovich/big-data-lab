from django.db import models
from datetime import datetime

# from .APIparsers.ApiModels import ArticleModel, ArticleTagsEnum


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)


class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)


class Member(TenantAwareModel):
    name = models.CharField(max_length=255)

# class ArticleModelDB(models.Model):
#     title = models.CharField(max_length=256, blank=True, null=True)
#    text = models.CharField(max_length=256, blank=True, null=True)
#   image_link = models.CharField(max_length=256, blank=True, null=True)
#   article_link = models.CharField(max_length=256, blank=True, null=True)
#   create_time = models.DateTimeField(default='1999-05-08 0:00')
#   tag = models.CharField(max_length=20)


#class DatabaseStorage:
#    @staticmethod
#    def save_news(article):
#        ArticleModelDB.objects.create(
#            title=article.title,
#            text=article.text,
#            image_link=article.image_link,
#            article_link=article.article_link,
#            create_time=article.last_update_obj,
#            tag=article.tag.name
#        )

#    @staticmethod
#    def get_articles(tag):
#        articles = []
#        if tag == ArticleTagsEnum.all:
#            db_articles = ArticleModelDB.objects.filter()
#        else:
#            db_articles = ArticleModelDB.objects.filter(tag=tag.name)
#        for model in db_articles:
#            article = ArticleModel(model.title, model.create_time, model.text, model.article_link)
#            article.image_link = model.image_link
#            article.tag = ArticleTagsEnum[model.tag]
#            articles.append(article)
#        return articles
