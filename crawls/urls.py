from django.urls import path

from . import views

app_name = 'crawls'
urlpatterns = [
    path('', views.FanPageList.as_view(), name='index')
    ]