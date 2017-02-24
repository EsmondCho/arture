from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.get_profile_page, name='get_profile_page'),

    url(r'^/newsfeed$', views.newsfeed, name='newsfeed'),

    url(r'^/profile_picture$', views.get_profile_picture, name='get_profile_picture'),
    url(r'^/profile_picture/upload$', views.upload_profile_picture, name='upload_profile_picture'),

    url(r'^/friends$', views.get_friend_list, name='get_friend_list'),
    url(r'^/friend_requests$', views.get_friend_request_list, name='get_friend_request_list'),
    url(r'^/friend_requests/create$', views.create_friend_request, name='create_friend_request'),
    url(r'^/friend_requests/(?P<request_id>\w+)/update$', views.response_to_friend_request, name='response_to_friend_request'),
    url(r'^/friend_requests/(?P<request_id>\w+)/delete$', views.delete_in_request_list, name='delete_in_request_list'),

    url(r'^/articles$', views.get_article_list, name='get_article_list'),
    url(r'^/articles/create$', views.create_article, name='create_article'),
    url(r'^/articles/(?P<article_id>\w+)/update$', views.update_article, name='update_article'),
    url(r'^/articles/(?P<article_id>\w+)/delete$', views.delete_article, name='delete_article'),

    url(r'^/articles/(?P<article_id>\w+)/comments$', views.get_comment_list, name='get_comment_list'),
    url(r'^/articles/(?P<article_id>\w+)/comments/create$', views.create_comment, name='create_comment'),
    url(r'^/articles/(?P<article_id>\w+)/comments/(?P<comment_id>\w+)/update$', views.update_comment, name='update_comment'),
    url(r'^/articles/(?P<article_id>\w+)/comments/(?P<comment_id>\w+)/delete$', views.delete_comment, name='delete_comment'),

]
