import ast
import datetime
import json

from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from users.forms import ImageUploadForm
from login.views import authenticated
from .models import Article, Comment, Arture, User, Request

# Need to define what is user


def datetime_to_json(ob):
    if isinstance(ob, datetime.datetime):
        return ob.__str__()


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
        dic['article_id'] = article.id
        dic['user_id'] = article.user_id
        dic['tag'] = article.tag # tag is Arture objects
        dic['text'] = article.text
        dic['image'] = 'http://192.168.1.209:80' + article.image.url if article.image else ""
        #dic['comment_list'] = json.dumps(serializers.serialize("json", article.comment_list), default=datetime_to_json),
        #dic['comment_list'] = article.comment_list
        comment_list = []
        comment_object_list = article.comment_list
        for comment_object in comment_object_list:
            comment_user = User.objects.get(id=comment_object.author)
            dic_ = {}
            dic_['name'] = comment_user.name
            dic_['comment'] = comment_object.comment
            dic_['registered_time'] = comment_object.registered_time
            dic_['image'] = 'http://192.168.1.209:80' + comment_user.pic.url
            comment_list.append(dic_.copy())
        dic['comment_list'] = comment_list
        #dic['registered_time'] = json.dumps(serializers.serialize("json", article.registered_time), default=datetime_to_json),
        dic['registered_time'] = article.registered_time
        article_list.append(dic.copy())

    follow_list = []
    follow_objectId_list = profile.arture_list
    for id in follow_objectId_list:
        arture = Arture.objects.get(id=id)
        dic = {}
        dic['title'] = arture.title
        dic['image'] = 'http://192.168.1.209:80' + arture.image.url if arture.image else ""
        dic['arture_id'] = arture.id
        dic['arture_type'] = arture.arture_type
        follow_list.append(dic.copy())

    friend_list = []
    friend_objectId_list = profile.friend_list
    for id in friend_objectId_list:
        friend = User.objects.get(id=id)
        dic = {}
        dic['name'] = friend.name
        dic['user_id'] = friend.id
        dic['pic'] = 'http://192.168.1.209:80'+friend.pic.url
        friend_list.append(dic.copy())

    return render(request, 'users/profile.html', { 'profile_objectId': user_id,
                                                    'profile_name': profile.name,
                                                    'profile_img_url': 'http://192.168.1.209'+profile.pic.url,
                                                    'profile_email': profile.email,
                                                    'user_objectId': user_objectId,
                                                    'user_name': user_name,
                                                    'login_token': login_token,
                                                    'is_mine': is_mine,
                                                    'is_friend': is_friend,
                                                    'is_request_sended': is_request_sended,
						                            'is_request_received': is_request_received,
                                                    'article_list': article_list,
                                                    'follow_list': follow_list,
                                                    'friend_list': friend_list,
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
        response_data = []

        for friend_id in friend_list:
            friend = User.objects.get(id=friend_id)
            dic = {}
            dic['friend_id'] = friend.id
            dic['name'] = friend.name
            dic['image'] = 'http://http://192.168.1.209:80' + friend.pic.url
            response_data.append(dic.copy())

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
            r = Request.objects.get(id=request_id)
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
                    """
                    ### requests to node.js ###
                    params = {}
                    res = requests.get('http://192.168.1.208:3000/api/v1/users/' + user.id + '/add_friend/' + friend.id, params=params)
                    print(res)
                    """
                    return HttpResponse(status=200)

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


def get_article_list(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "GET":
        article_list = Article.objects.filter(user_id=user_id)
        response_data = []

        for article in article_list:
            request_ = {}
            request_['article_id'] = article.id
            request_['user_id'] = article.user_id
            request_['tag'] = article.tag # response_data[article.id]['tag'] = serializers.serialize("json", article.tag)
            request_['text'] = article.text
            if article.image:
                request_['image'] = 'http://192.168.1.209:80' + article.image.url
            else:
                request_['image'] = None
            request_['comment_list'] = []
            for comment_object in article.comment_list:
                req = {}
                comment_user = User.objects.get(id=comment_object.author)
                req['user_id'] = comment_user.id
                req['name'] = comment_user.name
                req['comment'] = comment_object.comment
                req['registered_time'] = comment_object.registered_time
                request_['comment_list'].append(req.copy())
            request_['registered_time'] = article.registered_time
            response_data.append(request_.copy())

        return HttpResponse(json.dumps(response_data, default=datetime_to_json), content_type='application/json', status=200)
    return HttpResponseForbidden('Allowed only via GET')

@csrf_exempt
def create_article(request, user_id):

    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        form = ast.literal_eval(request.body)
        imageform = ImageUploadForm(request.POST, request.FILES)

        if Arture.objects.filter(title=form['tag']).count():
            arture = Arture.objects.get(title=form['tag'])
        else:
            arture = Arture.objects.get(title='default_arture')

        if imageform.is_valid():  # create article with image
            article = Article.objects.create(
                user_id=user_id,
                tag=arture,
                text=form['text'],
                image=imageform.cleaned_data['image'],
                comment_list=[],
            )
            article.save()
            user = User.objects.get(id=user_id)
            user.article_list.insert(0, article.id)
            user.save()
            """
            ### requests to node.js ###
            params = {}
            res = requests.get('http://192.168.1.208:3000/api/v1/users/' + user.id + '/create_article/' + article.id + '/tag/' + arture.id, params=params)
            print(res)
            """
            response_data = {}
            response_data['article_id'] = article.id
            return HttpResponse(json.dumps(response_data, default=datetime_to_json), content_type='application/json', status=201)

        else:  # create article without image
            article = Article.objects.create(
                user_id=user_id,
                tag=arture,
                text=form['text'],
                comment_list=[],
            )
            article.save()
            user = User.objects.get(id=user_id)
            user.article_list.insert(0, article.id)
            user.save()

            response_data = {}
            response_data['article_id'] = article.id
            return HttpResponse(json.dumps(response_data, default=datetime_to_json), content_type='application/json', status=201)
    return HttpResponseForbidden('Allowed only via POST')


def update_article(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "POST":
        form = request.POST
        imageform = ImageUploadForm(request.POST, request.FILES)

        if Arture.objects.filter(title=form['tag']).count():
            arture = Arture.objects.get(title=form['tag'])
        else:
            arture = Arture.objects.get(title='default_arture')


        if imageform.is_valid():  # update article with image
            article = Article.objects.get(id=article_id)
            article.tag = arture
            article.text = form['text']
            article.image = imageform.cleaned_data['image']
            article.save()
            return HttpResponse(status=201)

        else:  # update article without image
            article = Article.objects.get(id=article_id)
            article.tag = arture
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
                #user.save()
                return HttpResponse(status=200)

    return HttpResponseForbidden('Allowed only via DELETE')


def get_comment_list(request, user_id, article_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == "GET":
        comment_list = Article.objects.get(id=article_id).comment_list
        response_data = []

        for comment_object in comment_list:
            req = {}
            comment_user = User.objects.get(id=comment_object.author)
            req['user_id'] = comment_user.id
            req['name'] = comment_user.name
            req['comment'] = comment_object.comment
            req['registered_time'] = comment_object.registered_time
            response_data.append(req.copy())

        return HttpResponse(json.dumps(response_data, default=datetime_to_json), content_type='application/json', status=200)


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
        comment.save()

        article.comment_list.insert(0, comment)
        article.save()

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
        response_data = []

        for arture in arture_list:
            dic = {}
            dic['arture_id'] = arture.id
            dic['arture_title'] = arture.title
            dic['image'] = 'http://192.168.1.209:80' + arture.image.url
            dic['article_list'] = arture.article_list
            dic['user_list'] = arture.user_list
            dic['arture_type'] = arture.arture_type
            dic['description'] = arture.description
            dic['related_arture_list'] = arture.related_arture_list
            response_data.append(dic.copy())

        return HttpResponse(json.dumps(arture_list), content_type='application/json', status=200)
    return HttpResponseForbidden('Allowed only via GET')


def follow_arture(request, user_id):
    if not authenticated(request):
        return redirect('/login/')

    if request.method == 'POST':
        form = request.POST
        user = User.objects.get(id=user_id)
        user.arture_list.insert(0, form['arture_id'])
        user.save()

        arture = Arture.objects.get(id=form['arture_id'])
        arture.user_list.insert(0, user_id)
        arture.save()
        """
        ### requests to node.js ###
        params = {}
        res = requests.get('http://192.168.1.208:3000/api/v1/users/' + user.id + '/follow/' + arture.id, params=params)
        print(res)
        """
        return HttpResponse(status=200)
    return HttpResponseForbidden('Allowed only via POST')
