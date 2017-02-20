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
            one_user_reviews_url = 'http://movie.naver.com/movie/point/af/list.nhn?st=nickname&sword=' + td.get_text()
            one_user_reviews_source_code = requests.get(one_user_reviews_url)
            one_user_reviews_plain_text = one_user_reviews_source_code.text
            one_user_reviews_soup = BeautifulSoup(one_user_reviews_plain_text, 'lxml')

            user_name = one_user_reviews_soup.find('h5', class_='sub_tlt').get_text().split('****')[0]
            print(user_name)
            """
            for a in one_user_reviews_soup.find_all('div', class_='paging').select('a'):
                review_page_url = one_user_reviews_url + '&page=' + a.get_text()
                review_page_source_code = requests.get(review_page_url)
                review_page_plain_text = review_page_source_code.text
                review_page_soup = BeautifulSoup(review_page_plain_text, 'lxml')

                for review in review_page_soup.find_all('')






            ##### get movie_title and description #####
            arture_url = 'http://movie.naver.com' + link.get('href')
            arture_num = arture_url.split('=')[1]

            movie_source_code = requests.get(arture_url)
            movie_plain_text = movie_source_code.text
            movie_soup = BeautifulSoup(movie_plain_text, 'lxml')

            movie_title = movie_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
            movie_description = movie_soup.find_all('p', class_='con_tx')[0].get_text()
            f.write('<movie title>'+movie_title+'\n')
            f.write('<description>'+movie_description+'\n')

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

                f.write('<actor name>'+actor_name+'\n')
                f.write('<actor profile>'+actor_description+'\n')

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

            f.write('<director name>'+director_name+'\n')
            f.write('<director profile>'+director_description+'\n')
            """
            print('----')
        print('-------------------- This page : ' + str(page) + ' --------------------')
        page += 1


        f.close()

review_crawler(1)
