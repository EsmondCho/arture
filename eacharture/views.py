#-*- coding: utf-8 -*-

import requests
import json

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from users.models import Arture, User, Article
from login.views import authenticated


def artures_home(request):

    return render(request, 'eacharture/artures_home.html', {})


def get_arture(request, arture_id):

    arture = Arture.objects.get(id=arture_id)

    dic = {}
    dic['arture_title'] = arture.title
    dic['arture_image'] = arture.image
    dic['arture_id'] = arture.id

    for user_objectId in arture.user_list:
        if user_objectId == request.session.get('user_objectId', False):
            dic['is_following'] = True
            break
        dic['is_following'] = False

    related_arture_list = []
    for r_ in arture.related_arture_list:
        r = Arture.objects.get(id=r_)
        dic_ = {}
        dic_['r_title'] = r.title
        dic_['r_image'] = r.image
        dic_['r_id'] = r.id
        related_arture_list.append(dic_.copy())

    dic['related_arture_list'] = related_arture_list

    articles = []
    for article_objectId in arture.article_list:
        num = int(1)
        article = Article.objects.get(id=article_objectId)
        if User.objects.filter(id=article.user_id).count() == 0:
            user = User.objects.get(name='default_user')
        else:
            user = User.objects.get(id=article.user_id)
        dic_ = {}
        dic_['user_name'] = user.name
        dic_['id'] = user.id
        dic_['text'] = article.text
        dic_['image'] = "http://192.168.1.209:80/media/profile_pictures/default_picture/default.png"
        # dic_['comment_list'] = article.comment_list # 댓글 리스트는 호출하면 주는걸로
        dic_['registered_time'] = article.registered_time
        articles.append(dic_.copy())
        if num == 10:
            break
    dic['recent_articles'] = articles

    users = []
    for user in arture.user_list:
        num = int(1)
        user = User.objects.get(id=user)
        dic_ = {}
        dic_['user_name'] = user.name
        dic_['image'] = 'http://192.168.1.209' + user.pic.url
        dic_['object_id'] = user.id
        users.append(dic_.copy())
    dic['followwer_list'] = users

    return render(request, 'eacharture/each_arture.html', dic)


def follow_arture(request, arture_id):

    if request.method == "POST":
        form = request.POST

        arture = Arture.objects.get(id=arture_id)
        user = User.objects.get(id=form['user_id'])

        user.arture_list.insert(0, arture.id)
        user.save()

        arture.user_list.insert(0, user.id)
        arture.save()

        ### requests to node.js ###
        res = requests.get('http://192.168.1.208:3000/api/v1/users/' + user.id + '/follow/' + arture.id)
        print(res)

        return HttpResponse(status=200)
    else:
        return HttpResponseForbidden('Allowed only via POST')
