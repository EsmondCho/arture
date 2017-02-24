from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.artures_home, name='artures_home'),
    url(r'^/(?P<arture_id>\w+)$', views.get_arture, name='get_arture'),
    url(r'^/(?P<arture_id>\w+)/follow$', views.follow_arture, name='follow_arture'),
]
