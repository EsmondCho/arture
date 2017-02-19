import json, datetime
import pymongo
from bson.objectid import ObjectId

from django.core import serializers
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from users.forms import ImageUploadForm

from .models import Article, Comment, Arture, User, Request

from login.views import authenticated

from django.views.decorators.csrf import csrf_exempt

import ast

# Need to define what is user

def get_profile_page(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    profile = User.objects.get(id=user_id)
    user_objectId = request.session.get('user_objectId')
    user_name = request.session.get('user_name')
    login_token = request.session.get('login_token')

    is_mine = True if profile.name == user_name else False

    is_friend = False
    for friend in profile.friend_list:
        if friend == user_objectId:
            is_friend = True
    is_request_sended = False
    is_request_received = False

    article_list = []
    article_objectId_list = profile.article_list
    for id in article_objectId_list:
        article = Article.objects.get(id=id)
        dic = {}
        dic['article_id'] = id
        dic['user_id'] = article.user_id
        dic['tag'] = article.tag
        dic['text'] = article.text
        dic['image'] = 'http://192.168.1.209:80' + article.image.url if article.image is not None else ""
        dic['comment_list'] = json.dumps(serializers.serialize("json", article.comment_list), default=datetime_to_json),
        dic['registered_time'] = json.dumps(serializers.serialize("json", article.registered_time), default=datetime_to_json),
        article_list.append(dic.copy())

    follow_list = []
    follow_objectId_list = profile.arture_list
    for id in follow_objectId_list:
        arture = Arture.objects.get(id=id)
        dic['title'] = arture.title
        dic['image'] = arture.image.url if arture.image is not None else ""
        dic['article_list'] = arture.article_list
        dic['user_list'] = arture.user_list
        dic['arture_type'] = arture.arture_type
        dic['description'] = arture.description
        dic['related_arture_list'] = arture.related_arture_list
        follow_list.append(dic.copy())

    friend_list = []
    friend_objectId_list = profile.friend_list
    for id in friend_objectId_list:
        friend = User.objects.get(id=id)
        dic['name'] = friend.name
        dic['email'] = friend.email
        dic['gender'] = friend.gender
        dic['birth'] = friend.birth
        dic['address'] = friend.address
        dic['pic'] = friend.pic.url
        friend_list.append(dic.copy())

    return render(request, 'users/profile.html', { 'profile_objectId': user_id,
                                                    'profile_name': profile.name,
                                                    'profile_img_url' : 'http://192.168.1.209'+profile.pic.url,
                                                    'profile_email': profile.email,
                                                    'user_objectId' : user_objectId,
                                                    'user_name' : user_name,
                                                    'login_token' : login_token,
                                                    'is_mine' : is_mine,
                                                    'is_friend' : is_friend,
                                                    'is_request_sended' : is_request_sended,
						                            'is_request_received' : is_request_received,
                                                    'article_list' : article_list,
                                                    'follow_list' : follow_list,
                                                    'friend_list' : friend_list,
                                                  })


def newsfeed(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    user_objectId = request.session.get('user_objectId')
    user_name = request.session.get('user_name')
    login_token = request.session.get('login_token')
    user_img_url = User.objects.get(id=user_id).pic.url
    return render(request, 'users/newsfeed.html', {'user_objectId': user_objectId,
                                                  'user_name': user_name,
                                                  'login_token': login_token,
                                                  'user_img_url': user_img_url})


def upload_picture(request, user_id):
    if request.method == 'POST':
        f = request.POST
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            a = Article.objects.get(user_id=user_id)[0]
            a.image = form.cleaned_data['image']
            a.save()

            return HttpResponse('good')
        return HttpResponse('form invalid')
    return HttpResponseForbidden('allowed only via POST')


def get_profile_picture(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'GET':
        image_url = User.objects.get(id=user_id).pic.url
        return HttpResponse(image_url)
    return HttpResponseForbidden('allowed only via GET')


def upload_profile_picture(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.pic.delete()
            user.pic = form.cleaned_data['image']
            user.save()

            return redirect('/users/'+user_id)
        return HttpResponseForbidden('invalid form data')
    return HttpResponseForbidden('Allowed only via POST')


def get_friend_list(request, user_id):
    if request.method == 'GET':
        friend_list = User.objects.get(id=user_id).friend_list
        response_data = {}

        for friend_id in friend_list:
            friend = User.objects.get(id=friend_id)
            response_data[friend_id] = {}
            response_data[friend_id]['name'] = friend.name
            response_data[friend_id]['image'] = 'http://http://192.168.1.209:80' + friend.pic.url

        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


@csrf_exempt
def get_friend_request_list(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'GET':
        user_request_list = User.objects.get(id=user_id).friend_request_list
        response_data = []

        for r in user_request_list:
            user = User.objects.get(id=r.friend_id)
            request = {}
            request['user_id'] = user.id
            request['name'] = user.name
            request['image'] = 'http://192.168.1.209' + user.pic.url
            request['request_type'] = r.request_type
            request['request_id'] = r.id
            """
            response_data[r.id] = {}
            response_data[r.id]['user_id'] = user.id
            response_data[r.id]['name'] = user.name
            response_data[r.id]['image'] = 'http://http://192.168.1.209:80' + user.pic.url
            response_data[r.id]['request_type'] = r.request_type
            """
            response_data.append(request.copy())
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


def create_friend_request(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST': # create request
        form = request.POST

        # create request object & insert into user who made request
        request_waiting = Request.objects.create(
            friend_id = form['to_id'],
            request_type = 1
        )
        request_waiting.save()
        user_request = User.objects.get(id=user_id)
        user_request.friend_request_list.insert(0, request_waiting)
        user_request.save()

        # create request object & insert into user requested
        requested_waiting = Request.objects.create( # requested & waiting
            friend_id = user_id,
            request_type = 3
        )
        requested_waiting.save()
        user_requested = User.objects.get(id=form['to_id'])
        user_requested.friend_request_list.insert(0, requested_waiting)
        user_requested.save()

        return HttpResponse(status=200)
    return HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def response_to_friend_request(request, user_id, request_id):
    print("a")
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST': # response to request & insert into friend_list??
        form = ast.literal_eval(request.body)
        user = User.objects.get(id=user_id)
        if form['answer'] == "true":
            request_type = 4 # requested & accepted
        else:
            reqiest_type = 3

        if request_type == 4: # accepted
#            r = Request.objects.get(id=request_id)
            for r in user.friend_request_list:
                if r.id == request_id:
                    requested_object = Request.objects.create(
                        friend_id=r.friend_id,
                        request_type=4
                    )
                    requested_object.save()
                    user.friend_request_list.insert(0, requested_object)
                    user.friend_list.insert(0, r.friend_id)
                    user.save()

                    friend = User.objects.get(id=r.friend_id)

                    request_object = Request.objects.create(
                        friend_id=user.id,
                        request_type=2
                    )
                    request_object.save()
                    friend.friend_request_list.insert(0, request_object)
                    friend.friend_list.insert(0, user.id)
                    friend.save()

                    return HttpResponse(status=200)
        """
        for r in user.friend_request_list:
            if r.id == request_id:
                r.request_type = request_type
                if request_type == 4: # accepted
                    user.friend_list.insert(0, r.friend_id) # insert into friend_list ... encode error
                    friend = User.objects.get(id=r.friend_id)
                    friend.friend_list.insert(0, user.id)

                    for r_ in friend.friend_request_list:
                        if r_.friend_id == user_id:
                            r_.request_type == 2
                    friend.save()
                user.save()
                return HttpResponse(status=204)
        """
        return HttpResponseForbidden('Invalid request id')
    return HttpResponseForbidden('Allowed only via POST')

@csrf_exempt
def delete_in_request_list(request, user_id, request_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'DELETE': # delete request object in friend_request_list
        user = User.objects.get(id=user_id)
        for r in user.friend_request_list:
            if r.id == request_id:
                user.friend_request_list.remove(r)
                r.delete()
                user.save()
                return HttpResponse(status=204)
        return HttpResponseForbidden('Invalid request id')
    return HttpResponseForbidden('Allowed only via DELETE')


def datetime_to_json(ob):
    if isinstance(ob, datetime.datetime):
        return ob.__str__()


def get_article_list(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "GET":

        article_list = Article.objects.filter(user_id=user_id)
        response_data = {}

        for article in article_list:
            response_data[article.id] = {}
            response_data[article.id]['user_id'] = article.user_id
            response_data[article.id]['text'] = article.text
            response_data[article.id]['comment_list'] = serializers.serialize("json", article.comment_list)
            response_data[article.id]['emotion_list'] = article.emotion_list
            response_data[article.id]['tag'] = article.tag
            response_data[article.id]['registered_time'] = article.registered_time
            if article.image:
                response_data[article.id]['image'] = article.image.url
            else:
                response_data[article.id]['image'] = None

        return HttpResponse(json.dumps(response_data, default=datetime_to_json), content_type='application/json',
                            status=200)
    return HttpResponseForbidden('Allowed only via GET')

@csrf_exempt
def create_article(request, user_id):

    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        form = ast.literal_eval(request.body)
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():  # create article with image
            article = Article.objects.create(
                user_id=user_id,
                tag=form['tag'],
                text=form['text'],
                image=imageform.cleaned_data['image'],
                emotion_list=[],
                comment_list=[],
            )
            article.save()
            user = User.objects.get(id=user_id)
            user.article_list.insert(0, article.id)
            user.save()
            return HttpResponse(status=201)

        else:  # create article without image
            article = Article.objects.create(
                user_id=user_id,
                tag=form['tag'],
                text=form['text'],
                emotion_list=[],
                comment_list=[],
            )
            article.save()
            user = User.objects.get(id=user_id)
            user.article_list.insert(0, article.id)
            user.save()
            return HttpResponse(status=201)
    return HttpResponseForbidden('Allowed only via POST')


def update_article(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "POST":
        form = request.POST
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():  # update article with image
            article = Article.objects.get(id=article_id)
            article.tag = form['tag']
            article.text = form['text']
            article.image = imageform.cleaned_data['image']
            article.save()
            return HttpResponse(status=201)

        else:  # update article without image
            article = Article.objects.get(id=article_id)
            article.tag = form['tag']
            article.text = form['text']
            article.save()
            return HttpResponse(status=201)
    return HttpResponseForbidden('Allowed only via POST')


def delete_article(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "DELETE":
        article = Article.objects.get(id=article_id)
        article.delete()
        user = User.objects.get(id=user_id)

        for article in user.article_list:
            if article == article_id:
                user.article_list.remove(article)
                user.save()
                return HttpResponse(status=200)

    return HttpResponseForbidden('Allowed only via DELETE')


def get_comment_list(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "GET":
        comment_list = Article.objects.get(id=article_id).comment_list

        return HttpResponse(json.dumps(serializers.serialize("json", comment_list), default=datetime_to_json),
                            content_type='application/json', status=200)


def create_comment(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "POST":
        form = request.POST

        article = Article.objects.get(id=article_id)

        comment = Comment.objects.create(
            author=request.session.get('user_objectId', False),
            comment=form['comment']
        )

        return HttpResponse(status=201)
    return HttpResponseForbidden('Allowed only via POST')


def update_comment(request, user_id, article_id, comment_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "POST":
        form = request.POST

        comment = Comment.objects.filter(id=comment_id)
        comment.update(
            comment=form['comment']
        )

        article = Article.objects.get(id=article_id)
        for comment in article.comment_list:
            if comment.id == comment_id:
                comment.comment = form['comment']
                article.save()
                return HttpResponse(status=201)
        return HttpResponse('invalid comment id')
    return HttpResponseForbidden('Allowed only via POST')


def delete_comment(request, user_id, article_id, comment_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'DELETE':  # delete comment object in comment_list
        article = Article.objects.get(id=article_id)

        for comment in article.comment_list:
            if comment.id == comment_id:
                article.comment_list.remove(comment)
                comment.delete()
                article.save()
                return HttpResponse(status=201)
        return HttpResponseForbidden('Invalid comment_id')
    return HttpResponseForbidden('Allowed only via POST')


def get_following_arture_list(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'GET':
        arture_list = User.objects.get(id=user_id).arture_list

        return HttpResponse(json.dumps(arture_list), content_type='application/json', status=200)
    return HttpResponseForbidden('Allowed only via GET')

def follow_arture(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        form = request.POST
        user = User.objects.get(id=user_id)
        user.arture_list.insert(0, form['arture_id']).save()

        arture = Arture.objects.get(id=form['arture_id'])
        arture.user_list.insert(0, user_id).save()

        return HttpResponse(status=200)
    return HttpResponseForbidden('Allowed only via POST')
