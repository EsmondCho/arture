import os
import requests
import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def crawler(max_pages):
    f = codecs.open('t.text', 'w', 'utf-8')

    page = 1
    while page <= int(max_pages):
        url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170217&page=' + str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        main_soup = BeautifulSoup(main_plain_text, 'lxml')
        for link in main_soup.select('td > div > a'):
            ##### get movie_title and description #####
            arture_url = 'http://movie.naver.com' + link.get('href')
            arture_num = arture_url.split('=')[1]
            """
            movie_source_code = requests.get(arture_url)
            movie_plain_text = movie_source_code.text
            movie_soup = BeautifulSoup(movie_plain_text, 'lxml')

            movie_title = movie_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
            movie_description = movie_soup.find_all('p', class_='con_tx')[0].get_text()

            ##### get actor name and description #####
            artists_url = 'http://movie.naver.com/movie/bi/mi/detail.nhn?code=' + arture_num
            source_code = requests.get(artists_url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'lxml')

            for div in soup.find_all('div', class_='p_info'):
                actor_url = 'http://movie.naver.com' + div.select('a')[0].get('href')
                actor_source_code = requests.get(actor_url)
                actor_plain_text = actor_source_code.text
                actor_soup = BeautifulSoup(actor_plain_text, 'lxml')

                actor_name = actor_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
                if not actor_soup.find_all('div', class_='con_tx'):
                    actor_description = "no description"
                else:
                    if not actor_soup.find_all('div', class_='con_tx')[0].select('p'):
                        actor_description = actor_soup.find_all('div', class_='con_tx')[0].get_text()
                    else:
                        actor_description = actor_soup.find_all('div', class_='con_tx')[0].select('p')[0].get_text()

            ##### get director name and description #####
            director_url = 'http://movie.naver.com' + soup.find_all('div', class_='dir_product')[0].select('a')[0].get('href')
            director_source_code = requests.get(director_url)
            director_plain_text = director_source_code.text
            director_soup = BeautifulSoup(director_plain_text, 'lxml')

            director_name = director_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
            if not director_soup.find_all('div', class_='con_tx'):
                director_description = "no description"
            else:
                if not director_soup.find_all('div', class_='con_tx')[0].select('p'):
                    director_description = director_soup.find_all('div', class_='con_tx')[0].get_text()
                else:
                    director_description = director_soup.find_all('div', class_='con_tx')[0].select('p')[0].get_text()

            """

            ##### get review #####
            """
            reviews_url = 'http://movie.naver.com/movie/bi/mi/point.nhn?code=' + arture_num
            print('1')
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome('/usr/bin/chromedriver')
            print('2')
            driver.get(reviews_url)
            print('3')
            print(driver.page_source.endoce('utf-8'))
            print('4')
            driver.close()
            print('5')

            reviews_source_code = requests.get(reviews_url)
            reviews_plain_text = reviews_source_code.text
            f.write(reviews_plain_text)
            f.write('------------------------------------------------')
            reviews_soup = BeautifulSoup(reviews_plain_text, 'lxml')
            score_result = reviews_soup.find('div', class_='score_result')
            """
            print('------------------------------------------------')
        page += 1
        f.close()
crawler(1)
