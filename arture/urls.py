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
    url(r'^follow_making$', views.make_follow, name='make_follow'),
    url(r'^friend_making$', views.make_friend, name='make_friend'),
    url(r'^reset_userId$', views.reset_userId, name='reset_userId'),
    url(r'^insert_image_to_movie$', views.insert_image_to_movie, name='insert_image_to_movie'),
    url(r'^article_tag_object_to_objectId', views.article_tag_object_to_objectId, name='article_tag_object_to_objectId'),
    url(r'^change_id', views.change_id, name='change_id'),

    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^users/(?P<user_id>\w+)', include('users.urls', namespace='users')),
    url(r'^artures', include('eacharture.urls', namespace='eacharture')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]