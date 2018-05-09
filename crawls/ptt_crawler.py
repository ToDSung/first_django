import requests
from bs4 import BeautifulSoup

ptt_url = 'https://www.ptt.cc/'
article_list_information = []

index_page_source = requests.get(
    'https://www.ptt.cc/bbs/Gossiping/index.html', cookies={'over18': '1'})
soup = BeautifulSoup(index_page_source.text, 'lxml')
today = soup.select('div[class="date"]')[0].text

pages = 1
while pages:
    print('目前正在爬取第{}頁'.format(pages))
    old_index = (ptt_url+soup.select('a[class="btn wide"]')[1]['href'])
    index_page_source = requests.get(
        old_index, cookies={'over18': '1'})
    soup = BeautifulSoup(index_page_source.text, 'lxml')
    articles_list = soup.select(
        'div[class="r-list-container action-bar-margin bbs-screen"]')
    for article in articles_list[0].select('div[class="r-ent"]'):
        if article.a:
            push_boo = article.select('div[class="nrec"]')[0].text
            title = article.a.text
            page_url = (ptt_url + article.a['href'])
            date = article.select('div[class="date"]')[0].text

            if today == date:
                article_list_information.append(
                    [push_boo, title, page_url, date])
            else:
                break
    pages += 1

    print(date)
    if today == date:
        pass
    else:
        print('已爬取完成')
        break
return article_list_information
