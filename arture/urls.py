from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^admin$', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^users/(?P<user_id>\w+)/', include('users.urls', namespace='users')),
    url(r'^artures/(?P<arture_id>\w+)$', views.get_description, name='get_description'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]