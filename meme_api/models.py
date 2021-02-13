from django.db import models

# Create your models here.


class Meme(models.Model):
    '''
    class to create a model for a meme
    meme will have following attributes
    1) name of the author
    2) caption for the meme
    3) url for image source
    '''
    name = models.CharField(max_length=200, null=True)
    caption = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=100000, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
