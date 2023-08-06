from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vote/(?P<answer_id>[0-9]+)/$', views.vote, name='vote'),
]

