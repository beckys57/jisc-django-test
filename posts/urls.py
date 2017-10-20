from django.conf.urls import url
from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.list_all, name='list_all'),
    url(r'^(?P<post_id>\d+)/$', views.view_post, name='view_post'),
]