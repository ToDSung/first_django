from django.shortcuts import render
from django.views import generic

from .models import FanPage
# Create your views here.

class FanPageView(generic.ListView):
    template_name = 'crawls/index.html'
    context_object_name = 'fanpage_list'

    def get_queryset(self):
        fanpage_list = FanPage.objects.all()
        return fanpage_list