from django.urls import path

from . import views

app_name = 'crawls'
urlpatterns = [
    path('', views.FanPageView.as_view(), name='index'),
    ]