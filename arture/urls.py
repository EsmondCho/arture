from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^admin$', admin.site.urls),
    url(r'^$', views.home, name='home'),

    url(r'^arture_crawler/(?P<start_page>\d+)/(?P<finish_page>\d+)$', views.arture_crawler, name='arture_crawler'),
    url(r'^review_crawler/(?P<start_page>\d+)/(?P<finish_page>\d+)$', views.review_crawler, name='review_crawler'),

    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^users/(?P<user_id>\w+)', include('users.urls', namespace='users')),
    url(r'^artures/(?P<arture_id>\w+)$', views.get_description, name='get_description'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]