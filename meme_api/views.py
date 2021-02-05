from django.shortcuts import render
from .serializers import MemeSerializer
from .models import Meme
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status

'''
Creating various api_views
Here we use generic views as provided by django generic classes
'''


class ApiOverview(APIView):
    '''
    Api view to display info about all the
    api endpoints
    '''

    def get(self, request, format=None):
        api_urls = {
            'post a meme': '/memes',
            'get a list of meme': '/memes',
            'get a particular id': '/memes/<id>',
            'update a meme': '/memes/<id>'
        }
        return Response(api_urls)


class MemeListCreateView(APIView):
    '''
    Class based view which
    fetches list of latest 1000 memes for GET method
    adds a new meeme to database on POST method
    '''

    def get(self, request, format=None):
        # get latest 1000 memes which have been added to the data base
        Latest_memes = Meme.objects.order_by('date_created')[:1000]
        serializer = MemeSerializer(Latest_memes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # accept a meme
        serializer = MemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
