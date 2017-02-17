import json, datetime
import pymongo
from bson.objectid import ObjectId

from django.core import serializers
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from users.forms import ImageUploadForm

from .models import Article, Comment, Arture, User, Request

from login.views import authenticated


def newsfeed(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    user_objectId = request.session.get('user_objectId')
    user_email = request.session.get('user_email')
    user_name = request.session.get('user_name')
    login_token = request.session.get('login_token')

    return render(request, 'users/newsfeed.html', {'user_objectId': user_objectId,
                                                  'user_email': user_email,
                                                  'user_name': user_name,
                                                  'login_token': login_token
})


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
        image_url = 'http://192.168.56.1:8000' + User.objects.get(id=user_id).pic.url
        return redirect(image_url)
    return HttpResponseForbidden('allowed only via GET')


def upload_profile_picture(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        f = request.POST
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.pic.delete()
            user.pic = form.cleaned_data['image']
            user.save()
            return HttpResponse(status=200)
        return HttpResponseForbidden('invalid form data')
    return HttpResponseForbidden('Allowed only via POST')



def get_friend_list(request, user_id):
    if request.method == 'GET':
        friend_list = User.objects.get(id=user_id).friend_list

        return HttpResponse(json.dumps(friend_list), content_type='application/json', status=200)


def get_friend_request_list(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'GET':
        user_request_list = User.objects.get(id=user_id).friend_request_list
        response_data = {}

        for r in user_request_list:
            response_data[r.id] = {}
            response_data[r.id]['friend_id'] = r.friend_id
            response_data[r.id]['request_type'] = r.request_type

        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


def create_friend_request(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST': # create request
        form = request.POST

        # create request object & insert into user who made request
        request_waiting = Request.objects.create(
            friend_id = form['To_id'],
            request_type = 1
        )
        request_waiting.save()
        user_request = User.objects.get(id=user_id)
        user_request.friend_request_list.insert(0, request_waiting)
        user_request.save()

        # create request object & insert into user requested
        requested_waiting = Request.objects.create( # requested & waiting
            friend_id = user_id,
            request_type = 4
        )
        requested_waiting.save()
        user_requested = User.objects.get(id=form['To_id'])
        user_requested.friend_request_list.insert(0, requested_waiting)
        user_requested.save()

        return HttpResponse(status=200)
    return HttpResponseForbidden('Allowed only via POST')


def response_to_friend_request(request, user_id, request_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST': # response to request & insert into friend_list??
        form = request.POST
        user = User.objects.get(id=user_id)

        if form['answer'] == True:
            request_type = 5 # requested & accepted
        else:
            request_type = 6 # requested & rejected

        for r in user.friend_request_list:
            if r.id == request_id:
                r.request_type = request_type
                user.friend_list.insert(0, r.friend_id) # insert into friend_list ... encode error
                user.save()
                return HttpResponse(status=204)
        return HttpResponseForbidden('Invalid request id')
    return HttpResponseForbidden('Allowed only via POST')


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


def create_article(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        form = request.POST
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
