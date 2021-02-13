from rest_framework import serializers
from .models import Meme
from rest_framework.validators import UniqueTogetherValidator


class MemeSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize data for meme
    '''

    class Meta:
        # ToDo items belong to a parent list, and have an ordering defined
        # by the 'position' field. No two items in a given list may share
        # the same position.
        model = Meme
        fields = ['id', 'name', 'caption', 'url']
        # read_only_fields = ('is_active', 'is_staff')
        # read_only_fields = ('name',)
        # extra_kwargs = {
        #     'name': {'write_only': True}
        # }
