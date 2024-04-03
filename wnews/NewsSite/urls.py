from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    url(r'^filter_news', views.filter_news),
]