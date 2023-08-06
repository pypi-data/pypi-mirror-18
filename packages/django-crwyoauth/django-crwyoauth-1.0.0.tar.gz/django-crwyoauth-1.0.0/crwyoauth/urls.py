# encoding=utf-8
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^github$', GithubOauthView.as_view(), name='github_oauth'),
    url(r'^sina$', SinaOauthView.as_view(), name='sina_oauth'),
    url(r'^qq$', TencentOauthView.as_view(), name='sina_oauth'),
]
