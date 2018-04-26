from django.shortcuts import render
from django.views import generic

# Create your views here.

class FanPageList(generic.ListView):
    template_name = 'crawls/index.html'
    context_object_name = 'fanpage_list'