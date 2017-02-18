import requests
from bs4 import BeautifulSoup

def spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170217&page='+str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        for link in soup.select('td > div > a'):
            title = link.get('title')
            print(title)
        page += 1

spider(40)