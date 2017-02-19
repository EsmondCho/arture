import requests

from bs4 import BeautifulSoup
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from login.views import authenticated
from users.models import Arture


def home(request):
    user_objectId = request.session.get('user_objectId')
    if authenticated(request):
        return redirect('/users/' + user_objectId + '/newsfeed')
    else:
        return render(request, 'login/index.html', {})


def get_description(request, arture_id):
    if not authenticated(request):
        return redirect('/login/')

    description = Arture.objects.get(id=arture_id).description

    return HttpResponse(description)


def crawler(request, max_pages):
    page = 1
    while page <= int(max_pages):
        url = 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20170217&page='+str(page)
        main_source_code = requests.get(url)
        main_plain_text = main_source_code.text
        soup = BeautifulSoup(main_plain_text, 'lxml')
        for link in soup.select('td > div > a'):
            title = link.get('title')
            arture_url = 'http://movie.naver.com' + link.get('href')
            arture_num = arture_url.split('=')[1]

            source_code = requests.get(arture_url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'lxml')

            ### arture(movie) create ###
            if Arture.objects.filter(title=title).count() == 0:
                arture = Arture.objects.create(
                    title=title,
                    arture_type=False,
                    description=soup.select('div > div > div > div > div > div > div > div > p')[0].get_text(),
                    related_arture_list=[],
                    article_list=[],
                    user_list=[]
                )
                arture.save()

            ### arture(director, actor) create ###

        page += 1
    return HttpResponse('good')
