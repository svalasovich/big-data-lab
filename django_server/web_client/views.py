from django import forms
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .managers import DatabaseClient, TagsEnum


database_client = DatabaseClient()


def home(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        articles = database_client.load_news(request.tenant.feeder_name)
        return render(request, "news_list.html", locals())


def select_tag(request):
    for item in TagsEnum:
        if item.name in request.GET:
            articles = database_client.load_news(request.tenant.feeder_name, tag=item.name)
    return render(request, "news_list.html", locals())


def registration(request):
    if request.method == 'POST':
        if 'submit' in request.POST:
            new_username = request.POST['username_id']
            new_email = request.POST['email_id']
            new_password = request.POST['password_id']

            if new_email and User.objects.filter(email=new_email).exclude(username=new_username).exists():
                raise forms.ValidationError(u'Email addresses must be unique.')

            new_user = User.objects.create_user(username=new_username,
                                                email=new_email,
                                                password=new_password)
            new_user.save()
        return redirect("/login")
    else:
        return render(request, 'registration.html')


def login_action(request):
    if 'registration' in request.GET:
        return redirect("/registration")
    else:
        print(dict(request.POST.items()))
        if 'login' in request.POST and 'email_id' in request.POST and 'password_id' in request.POST:
            cur_email = request.POST['email_id']
            cur_password = request.POST['password_id']
            cur_user = User.objects.get(email=cur_email)
            if cur_user is not None:
                user = authenticate(username=cur_user.username, password=cur_password)
                print(user)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("/home")
                else:
                    print('User not found!')
        return render(request, "login.html")


def logout_action(request):
    print('logout')
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login")
