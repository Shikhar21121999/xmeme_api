from django.shortcuts import render
from .serializers import MemeSerializer
from .models import Meme
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from django.http import Http404
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

'''
Creating various api_views
Here we use generic views as provided by django generic classes
'''


class MemeListCreateView(APIView):
    '''
    Class based view which
    fetches list of latest 1000 memes for GET method
    adds a new meeme to database on POST method
    '''

    def get(self, request, format=None):
        '''
        get latest 100 memes added to the database
        '''
        # get latest 1000 memes which have been added to the data base
        Latest_memes = Meme.objects.order_by('-date_created')[:100]
        serializer = MemeSerializer(Latest_memes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        '''
        add a new meme to the database
        '''
        # serialize and validate the data
        print('inside post')
        serializer = MemeSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print('data valid')
            data = serializer.validated_data
            # print(data)
            dup_obj = Meme.objects.filter(
                name=data['name'], url=data['url'], caption=data['caption'])
            print(dup_obj)
            if len(dup_obj) == 0:
                print("good post")
                serializer.save()
                # retrun id of the created meme as json response
                mydict = {
                    'id': serializer.data['id']
                }
                return Response(mydict, status=status.HTTP_201_CREATED)
            else:
                resdict = {
                    'error': 'A meme with exactly same data exist'
                }
                return Response(resdict, status=status.HTTP_400_BAD_REQUEST)
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
        '''
        get detail of a particular meme given by id
        '''
        # method to serve get request with
        # info about a meme with given id
        meme = self.get_object(pk)
        serializer = MemeSerializer(meme)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        '''
        make changes to an already existing meme via patch
        '''
        # method to serve patch request
        # by updating the contents of meme
        # with given id
        memetobeupdated = self.get_object(pk)
        print(request.data)
        serializer = MemeSerializer(
            memetobeupdated, data=request.data, partial=True)
        if serializer.is_valid():
            # remove name field so that name cannot be updated
            rem_field = serializer.validated_data.pop('name', None)
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        print("serializer is invalid")
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        meme = self.get_object(pk)
        meme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
