#-*- coding: utf-8 -*-

import requests
import codecs
from bs4 import BeautifulSoup


def review_crawler(max_pages):
    f = codecs.open('review_crawling.text', 'w', 'utf-8')

    page = 1
    while page <= int(max_pages):
        url = 'http://movie.naver.com/movie/point/af/list.nhn?&page=' + str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        main_soup = BeautifulSoup(main_plain_text, 'lxml')
        for td in main_soup.find_all('td', class_='ac num'):

            ##### get User and Article objects from reviews #####
            ### get user name ###
            one_user_reviews_url = 'http://movie.naver.com/movie/point/af/list.nhn?st=nickname&sword=' + td.get_text()
            one_user_reviews_source_code = requests.get(one_user_reviews_url)
            one_user_reviews_plain_text = one_user_reviews_source_code.text
            one_user_reviews_soup = BeautifulSoup(one_user_reviews_plain_text, 'lxml')

            user_name = one_user_reviews_soup.find('h5', class_='sub_tlt').get_text().split('****')[0]
            user_email = user_name + '@naver.com'
            print("<<<< " + user_name + " >>>>")

            ### get each movie_review's point, movie title, comment from one user ###
            for a in one_user_reviews_soup.find_all('div', class_='paging')[0].select('a'):
                if a.get_text() == '다음'.decode('utf-8'):
                    break
                print('reviews page : ' + a.get_text())

                review_page_url = one_user_reviews_url + '&page=' + a.get_text()
                review_page_source_code = requests.get(review_page_url)
                review_page_plain_text = review_page_source_code.text
                review_page_soup = BeautifulSoup(review_page_plain_text, 'lxml')

                for tr in review_page_soup.find('tbody').find_all('tr'):
                    point = tr.find('td', class_='point').get_text()
                    movie_title_and_comment = tr.find('td', class_='title')
                    movie_title = movie_title_and_comment.select('a')[0].get_text()
                    movie_comment = movie_title_and_comment.get_text().split(movie_title)[1].split('신고'.decode('utf-8'))[0].strip()
                    print('point : ' + point)
                    print('movie title : ' + movie_title)
                    print('movie comment : ' + movie_comment)
                    print('---')

                print("!!!!change one user's review page!!!!")
            print('-------------------------')
        print('-------------------- This page : ' + str(page) + ' --------------------')
        page += 1
    f.close()

review_crawler(1)
