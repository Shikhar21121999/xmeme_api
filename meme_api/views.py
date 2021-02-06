from django.shortcuts import render
from .serializers import MemeSerializer
from .models import Meme
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from django.http import Http404

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
        # serialize and validate the data
        print(request.query_params)
        print("next is request.data")
        print(request.data)
        serializer = MemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # retrun id of the created meme as json response
            mydict = {
                'id': serializer.data['id']
            }
            return Response(mydict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    '''
    Class based view to get detail of a meme
    with a particular id with get request
    and also make changes to it with patch request
    '''

    def get_object(self, pk):
        # method to check and return
        # if a meme with given id exists
        try:
            return Meme.objects.get(id=pk)
        except Meme.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # method to serve get request with
        # info about a meme with given id
        meme = self.get_object(pk)
        serializer = MemeSerializer(meme)
        return Response(serializer.data)

    def patch(self, request, pk):
        # method to serve patch request
        # by updating the contents of meme
        # with given id
        memetobeupdated = self.get_object(pk)
        serializer = MemeSerializer(
            memetobeupdated, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)
