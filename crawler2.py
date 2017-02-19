#-*- coding: utf-8 -*-

import requests

from bs4 import BeautifulSoup


def crawler(max_pages):
    page = 1
    while page <= max_pages:
        url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170217&page=' + str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        main_soup = BeautifulSoup(main_plain_text, 'lxml')
        for link in main_soup.select('td > div > a'):
            title = link.get('title')
            arture_url = 'http://movie.naver.com' + link.get('href')
            arture_num = arture_url.split('=')[1]

            source_code = requests.get(arture_url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'lxml')
            #print(soup)
            ps = soup.find_all("p",class_="con_tx")
            result = ""
            check = True
            for content in ps[0].contents:
               if check == True:
                   s = unicode(content).encode('utf-8')
                   result += s[0:-1]
                   check = False
               elif check == False:
                   check = True 
            print(result)
            print('---------------------------------------------------------------------------')
            break
        page += 1
        break
crawler(1)
