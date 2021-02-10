'''
Creating various endpoints for the api
'''

from django.urls import path, include
from meme_api.views import MemeListCreateView, DetailView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('memes', MemeListCreateView.as_view(), name='memes'),
    path('memes/<str:pk>', DetailView.as_view(), name='memes_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
