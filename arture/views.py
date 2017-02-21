#-*- coding: utf-8 -*-

import codecs
import random

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.models import Arture, User, Article
from login.views import authenticated


def home(request):
    """
    user_objectId = request.session.get('user_objectId', False)
    if user_objectId:
        if authenticated(request):
            return redirect('/users/' + user_objectId + '/newsfeed')
        else:
            return render(request, 'login/index.html', {})
    """
    return render(request, 'login/index.html', {})


def get_description(request, arture_id):
    if not authenticated(request):
        return redirect('/login/')

    description = Arture.objects.get(id=arture_id).description

    return HttpResponse(description)


def arture_crawler(request, start_page, finish_page):
    page = int(start_page)
    while page <= int(finish_page):
        url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170219&page=' + str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        main_soup = BeautifulSoup(main_plain_text, 'lxml')
        for idx, link in enumerate(main_soup.select('td > div > a')):

            ##### get movie_title and description #####
            arture_url = 'http://movie.naver.com' + link.get('href')
            arture_num = arture_url.split('=')[1]

            movie_source_code = requests.get(arture_url)
            movie_plain_text = movie_source_code.text
            movie_soup = BeautifulSoup(movie_plain_text, 'lxml')

            if movie_soup.find('h3', class_='h_movie'):
                movie_title = movie_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
                if movie_soup.find_all('div', class_='story_area'):
                    movie_description = movie_soup.find_all('p', class_='con_tx')[0].get_text()
                else:
                    movie_description = "no description"
            else:
                continue
            print('move name : ' + movie_title)

            ##### insert movie_title, movie_description into DB
            ### new movie ###
            if Arture.objects.filter(title=movie_title).count() == 0:
                movie = Arture.objects.create(
                    title=movie_title,
                    article_list=[],
                    user_list=[],
                    image="",
                    arture_type=False,
                    description=movie_description,
                    related_arture_list=[]
                )
                movie.save()
            ### existing movie ###
            movie = Arture.objects.get(title=movie_title)

            ### if article that tagging this movie exist ###


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

                if Arture.objects.filter(title=actor_name).filter(arture_type=True).count() == 0: # if it is not existed actor
                    actor = Arture.objects.create(
                        title=actor_name,
                        article_list=[],
                        user_list=[],
                        image="",
                        arture_type=True,
                        description=actor_description,
                        related_arture_list=[movie.id]
                    )
                    actor.save()
                else: # existing actor
                    actor = Arture.objects.get(title=actor_name, arture_type=True)
                    actor.related_arture_list.insert(0, movie.id)
                    actor.save()

                movie.related_arture_list.insert(0, actor.id)
                movie.save()
            ##### get director name and description #####
            if soup.find_all('div', class_='dir_product'):
                director_url = 'http://movie.naver.com' + soup.find_all('div', class_='dir_product')[0].select('a')[0].get('href')
                director_source_code = requests.get(director_url)
                director_plain_text = director_source_code.text
                director_soup = BeautifulSoup(director_plain_text, 'lxml')
            else:
                continue

            director_name = director_soup.find_all('h3', class_='h_movie')[0].select('a')[0].get_text()
            if not director_soup.find_all('div', class_='con_tx'):
                director_description = "no description"
            else:
                if not director_soup.find_all('div', class_='con_tx')[0].select('p'):
                    director_description = director_soup.find_all('div', class_='con_tx')[0].get_text()
                else:
                    director_description = director_soup.find_all('div', class_='con_tx')[0].select('p')[0].get_text()

            if Arture.objects.filter(title=director_name).filter(arture_type=True).count() == 0:  # if it is not existed director
                director = Arture.objects.create(
                    title=director_name,
                    article_list=[],
                    user_list=[],
                    image="",
                    arture_type=True,
                    description=director_description,
                    related_arture_list=[movie.id]
                )
                director.save()
            else:  # existing actor
                director = Arture.objects.get(title=director_name, arture_type=True)
                director.related_arture_list.insert(0, movie.id)
                director.save()

            movie.related_arture_list.insert(0, director.id)
            movie.save()

            print(idx)
        print('-------------------- This page : '+str(page)+' --------------------')
        page += 1

    return HttpResponse('good')


def review_crawler(request, start_page, finish_page):
    ### get user_name_list from file ###
    user_name_list = []
    name_file = codecs.open('/home/smilegate/auto_client/user_name_list', 'r', 'utf-8')
    lines = name_file.readlines()
    for line in lines:
        user_name_list.insert(0, line)

    ### set gender_list
    gender_list = [True, False]

    page = int(start_page)
    while page <= int(finish_page):
        url = 'http://movie.naver.com/movie/point/af/list.nhn?&page=' + str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        main_soup = BeautifulSoup(main_plain_text, 'lxml')
        for idx, td in enumerate(main_soup.find_all('td', class_='ac num')):

            ##### get User and Article objects from reviews #####
            ### get user name ###
            one_user_reviews_url = 'http://movie.naver.com/movie/point/af/list.nhn?st=nickname&sword=' + td.get_text()
            one_user_reviews_source_code = requests.get(one_user_reviews_url)
            one_user_reviews_plain_text = one_user_reviews_source_code.text
            one_user_reviews_soup = BeautifulSoup(one_user_reviews_plain_text, 'lxml')

            user_email = one_user_reviews_soup.find('h5', class_='sub_tlt').get_text().split('****')[0] + '@auto.com'

            ### new user ###
            if User.objects.filter(email=user_email).count() == 0:
                user = User.objects.create(
                    name=random.choice(user_name_list),
                    email=user_email,
                    pwd='asdf',
                    gender=random.choice(gender_list),
                    birth='20170220',
                    friend_list=[],
                    friend_request_list=[],
                    arture_list=[],
                    article_list=[]
                )
                user.save()
            ### existing user ###
            else:
                user = User.objects.get(email=user_email)

            ### get each movie_review's point, movie title, comment from one user ###
            for a in one_user_reviews_soup.find_all('div', class_='paging')[0].select('a'):
                if a.get_text() == '다음'.decode('utf-8'):
                    break
                print("one user's reviews page : " + a.get_text())

                review_page_url = one_user_reviews_url + '&page=' + a.get_text()
                review_page_source_code = requests.get(review_page_url)
                review_page_plain_text = review_page_source_code.text
                review_page_soup = BeautifulSoup(review_page_plain_text, 'lxml')

                for tr in review_page_soup.find('tbody').find_all('tr'):
                    point = tr.find('td', class_='point').get_text()
                    review_number = tr.find('td', class_='ac num').get_text()
                    movie_title_and_comment = tr.find('td', class_='title')
                    movie_title = movie_title_and_comment.select('a')[0].get_text()
                    movie_comment = movie_title_and_comment.get_text().split(movie_title)[1].split('신고'.decode('utf-8'))[0].strip()

                    ### new arture ###
                    if Arture.objects.filter(title=movie_title).count() == 0:
                        arture = Arture.objects.get(title='out_of_top_movie_2000_default')
                    ### existing arture ##
                    else:
                        arture = Arture.objects.filter(title=movie_title)[0]

                    ### new article ###
                    if Article.objects.filter(naver_review_number=review_number).count() == 0:
                        article = Article.objects.create(
                            user_id=user.id,
                            tag=arture,
                            text=movie_comment,
                            comment_list=[],
                            naver_review_number=review_number
                        )
                        article.save()
                        ### insert article into article_list of arture
                        arture.article_list.insert(0, article.id)
                        arture.save()
                        ### insert article into article_list of User
                        user.article_list.insert(0, article.id)
                        user.save()
                    ### existing article ###
                    else:
                        continue

            print('-----------------------------------' + str(idx))
        print('---------------------------------------------- This page : ' + str(page))
        page += 1

    return HttpResponse('good')
