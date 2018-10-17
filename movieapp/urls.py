from django.conf.urls import url

from .views import *
from utils.auth import GetJWT

urlpatterns = [
    url('^$', PingAPI.as_view(), name='ping'),
    url('^ping/?$', PingAPI.as_view(), name='ping'),
    url('^auth/?$', GetJWT.as_view(), name='auth'),
    url('^search/?$', SearchAPI.as_view(), name='search'),
    url('^movie/?(?P<movieid>[0-9]+)?/?$', MovieAPI.as_view(), name='movie'),
]