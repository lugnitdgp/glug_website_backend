from rest_framework import serializers
from blog import models

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id','title','thumbnail_image','content_body')