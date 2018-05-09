from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse

from .fb_crawler import fb_crawler
from .models import Article, FanPage

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


class FanPageForm(ModelForm):
    class Meta:
        model = FanPage
        fields = ['name']


def add(request):
    if request.method == 'POST':
        form = FanPageForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            FanPage.objects.create(name=name)
            FanPage.save
            fanpage_list = FanPage.objects.all()
            return HttpResponseRedirect('/crawls/')
        return HttpResponse("The input data type doesn't supported")
        # return HttpResponseRedirect('/fanpage/' + str(new_article.pk))


def crawl(request, fanpage_id):
    fanpage = FanPage.objects.get(pk=fanpage_id)
    try:
        imformation_list = fb_crawler(fanpage_id, fanpage)
    except:
        return HttpResponse('The facebook token already expired')
    for row in imformation_list:
        Article.objects.create(fanpage_id=fanpage_id, text=row[0], time=row[1])
    Article.save
    return HttpResponseRedirect('/crawls/')


def delete_crawled_data(request, fanpage_id):
    Article.objects.filter(fanpage_id=fanpage_id).delete()
    return HttpResponseRedirect('/crawls/')


def delete_fanpage(request, fanpage_id):
    print(fanpage_id)
    FanPage.objects.filter(id=fanpage_id).delete()

    # 目前看來沒區別研究寫法
    # return render(request, reverse())
    return HttpResponseRedirect(reverse('crawls:index'))
    # return redirect('/crawls/')
