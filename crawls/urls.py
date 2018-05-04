# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = 'crawls'
urlpatterns = [
    path('', views.FanPageView.as_view(), name='index'),
    path('add', views.add, name='add'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('<int:fanpage_id>/crawl', views.crawl, name='crawl'),
    path('<int:fanpage_id>/delete', views.delete_crawled_data, name='delete_crawled_data'),
    path('<int:fanpage_id>/delete2', views.delete_fanpage, name='delete_fanpage')
    ]