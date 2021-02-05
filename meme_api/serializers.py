from rest_framework import serializers
from .models import Meme

class MemeSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize data for meme
    '''
    class Meta:
        model=Meme
        fields=['id','name','caption','url']

