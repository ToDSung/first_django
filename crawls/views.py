from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import FanPage, Article
from .fb_crawler import fb_crawler
# Create your views here.

class FanPageView(generic.ListView):
    template_name = 'crawls/index.html'
    context_object_name = 'fanpage_list'

    def get_queryset(self):
        fanpage_list = FanPage.objects.all()
        return fanpage_list

class DetailView(generic.DetailView):
    model = FanPage
    template_name = 'crawls/detail.html'

def fbcrawl(request):
    imformation_list = fb_crawler()
    
    for row in imformation_list:
        Article.objects.create(fanpage_id=1,text=row[0], time=row[1])
    Article.save
    
    return HttpResponse ("The fb crawler are already finished!")