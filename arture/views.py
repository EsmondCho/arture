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
