# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = 'crawls'
urlpatterns = [
    path('', views.FanPageView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('fbcrawl', views.fbcrawl, name='fbcrawl'),
    ]