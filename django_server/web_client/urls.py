from django.urls import path
from . import views

app_name = 'web_client'

urlpatterns = [
    path('select_tag', views.select_tag),
    path('login', views.login_action),
    path('logout', views.logout_action),
    path('registration', views.registration),
    path('home', views.home),
    path('', views.home, name='home'),
]
