'''
Creating various endpoints for the api
'''

from django.urls import path, include
from meme_api.views import ApiOverview, MemeListCreateView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', ApiOverview.as_view(), name='api_overview'),
    path('memes', MemeListCreateView.as_view(), name='memes'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
