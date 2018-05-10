from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse

from .fb_crawler import fb_crawler
from .ptt_crawler import ptt_crawler
from .models import Board, FacebookArticle, FanPage, PttArticle

# Create your views here.


class FanPageView(generic.ListView):
    template_name = 'crawls/facebook_index.html'
    context_object_name = 'fanpage_list'

    def get_queryset(self):
        fanpage_list = FanPage.objects.all()
        return fanpage_list


class DetailView(generic.DetailView):
    model = FanPage
    template_name = 'crawls/facebook_detail.html'


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
            return HttpResponseRedirect(reverse('crawls:facebook_index'))
        return HttpResponse("The input data type doesn't supported")
        # return HttpResponseRedirect('/fanpage/' + str(new_article.pk))


def crawl(request, fanpage_id):
    fanpage = FanPage.objects.get(pk=fanpage_id)
    try:
        imformation_list = fb_crawler(fanpage_id, fanpage)
    except:
        return HttpResponse('The facebook token already expired')
    for row in imformation_list:
        FacebookArticle.objects.create(
            fanpage_id=fanpage_id, text=row[0], time=row[1])
    FacebookArticle.save
    return HttpResponseRedirect(reverse('crawls:facebook_index'))


def delete_crawled_data(request, fanpage_id):
    FacebookArticle.objects.filter(fanpage_id=fanpage_id).delete()
    return HttpResponseRedirect(reverse('crawls:facebook_index'))


def delete_fanpage(request, fanpage_id):
    FanPage.objects.filter(id=fanpage_id).delete()

    # 目前看來沒區別研究寫法
    # return render(request, reverse())
    return HttpResponseRedirect(reverse('crawls:facebook_index'))
    # return redirect('/crawls/')


class BoardView(generic.ListView):
    template_name = 'crawls/ptt_index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        board_list = Board.objects.all()
        return board_list


class PTTDetailView(generic.DetailView):
    model = Board
    template_name = 'crawls/ptt_detail.html'


class PTTBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']


def add_ptt_board(request):
    if request.method == 'POST':
        form = PTTBoardForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            Board.objects.create(name=name)
            Board.save
            Board_list = Board.objects.all()
            return HttpResponseRedirect(reverse('crawls:ptt_index'))
        return HttpResponse("The input data type doesn't supported")
        # return HttpResponseRedirect('/fanpage/' + str(new_article.pk))



def crawl_ptt_data(request, board_id):
    board = Board.objects.get(pk=board_id)
    imformation_list = ptt_crawler(board_id, board.name)
    for row in imformation_list:
        PttArticle.objects.create(
            board_id=board_id, title=row[0], push_boo=row[1], date=row[2], url=row[3])
    PttArticle.save
    return HttpResponseRedirect(reverse('crawls:ptt_index'))


def delete_ptt_data(request, board_id):
    PttArticle.objects.filter(board_id=board_id).delete()
    return HttpResponseRedirect(reverse('crawls:ptt_index'))


def delete_board(request, board_id):
    Board.objects.filter(id=board_id).delete()

    # 目前看來沒區別研究寫法
    # return render(request, reverse())
    return HttpResponseRedirect(reverse('crawls:ptt_index'))
    # return redirect('/crawls/')
