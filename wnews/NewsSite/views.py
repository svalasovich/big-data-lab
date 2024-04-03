import sched, time

from threading import Thread
from django.shortcuts import render

#from .MachineLearning.SvmLib import SvmManager
#from .MachineLearning.TextManager import TextManager
#from .APIparsers.ApiModels import ArticleTagsEnum
#from .models import DatabaseStorage

#update_thread = None
#news_scheduler = sched.scheduler(time.time, time.sleep)

#text_manager = TextManager()
#news_storage = DatabaseStorage()
#svm_manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.economy, ArticleTagsEnum.science,
                         #ArticleTagsEnum.musics, ArticleTagsEnum.films, ArticleTagsEnum.politics)

#svm_dicts = svm_manager.load_add_svm_dicts()


def home(request):
    #svm_manager.load_all_svm_states()

    #load_first_articles(2000)

    #update_thread = Thread(target=run_news_updates)
    #update_thread.start()

    #articles = news_storage.get_articles(ArticleTagsEnum.all)
    #print("Count articles:", len(articles))
    return render(request, "news_list.html", locals())


def filter_news(request):
    for item in ArticleTagsEnum:
        if item.name in request.GET:
            articles = news_storage.get_articles(item)
    return render(request, "news_list.html", locals())


def load_first_articles(count):
    articles, _ = text_manager.get_articles(ArticleTagsEnum.all, count)
    predict_articles(articles)


def predict_articles(articles):
    for article in articles:
        article.tag = svm_manager.predict_article(article.full_text, svm_dicts)
        news_storage.save_news(article)


def run_news_updates():
    update_news()
    news_scheduler.run()


def update_news():
    articles = text_manager.get_new_articles(ArticleTagsEnum.all)

    if len(articles) > 0:
        predict_articles(articles)
        print("New news has been saving")
    else:
        print("New news not be found")

    news_scheduler.enter(300, 1, update_news)

