from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse

from .fb_crawler import fb_crawler
from .ptt_crawler import ptt_crawler
from .models import Board, FacebookArticle, FanPage, PttArticle

'''
可以用如下方法限制request傳入要求的方法
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def my_view(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    pass    
'''
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


"""
class FanPageForm(ModelForm):
繼承ModelForm 可以不用在view建立form類別
效果類似下面
class FanPageForm(forms.Form):
    name = forms.CharField(max_length=30)
也有error_message的方法可以調用
用這種寫法更改顯示的欄位樣板
    widgets = {
        'name': Textarea(attrs={'cols': 80, 'rows': 20}),
    }
"""
class FanPageForm(ModelForm):
    class Meta:
        model = FanPage
        fields = ['name']
        #fields = '__all__' 取用全部的欄位


def add(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
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
    return redirect('crawls:facebook_index')
    # return HttpResponseRedirect(reverse('crawls:facebook_index'))


def delete_fanpage(request, fanpage_id):
    FanPage.objects.filter(id=fanpage_id).delete()
    return HttpResponseRedirect(reverse('crawls:facebook_index'))


class BoardView(generic.ListView):
    template_name = 'crawls/ptt_index.html'
    context_object_name = 'board_list'

    def get_queryset(self):
        board_list = Board.objects.all()
        return board_list


'''
class PTTDetailView(generic.DetailView):
    model = Board
    template_name = 'crawls/ptt_detail.html'
'''


class PTTBoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name']


def show_article(request, board_id):
    board_list = Board.objects.filter(id=board_id)
    article_list = PttArticle.objects.filter(
        board_id=board_id).order_by('-date')
    return render(request, 'crawls/ptt_detail.html', {'board_list': board_list, 'article_list': article_list})


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
    PttArticle.objects.filter(board_id=board_id).delete()
    for row in imformation_list:
        PttArticle.objects.create(
            board_id=board_id, title=row[0], push_boo=row[1], date=row[2], url=row[3])
    PttArticle.save
    return HttpResponseRedirect(reverse('crawls:ptt_index'))


def delete_ptt_data(request, board_id):
    PttArticle.objects.filter(board_id=board_id).delete()
    # return redirect('crawls:ptt_index')
    # return redirect('/crawls/ptt/')
    return HttpResponseRedirect(reverse('crawls:ptt_index'))


def delete_board(request, board_id):
    Board.objects.filter(id=board_id).delete()

    return HttpResponseRedirect(reverse('crawls:ptt_index'))


'''
    Q: 研究各種 return 渲染回傳方法    

    render 後面必須要有request參數 reverse() 用做url尋找對應的view執行
    return render(request, reverse())
    
    #直接嘗試執行某個 view 方法
    return redirect('crawls:ptt_index')
    
    #用硬解碼的方式重新導向至指定 template ##注意這邊的網址前面仍有 / 
    return redirect('/crawls/ptt/')

    #redirecet 結合 reverse 的用法
    return HttpResponseRedirect(reverse('crawls:ptt_index'))
'''
