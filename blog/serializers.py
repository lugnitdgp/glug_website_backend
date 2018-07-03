from rest_framework import serializers
from blog import models

class PostSerializers(serializers.ModelSerializer):
    show_bool = serializers.SerializerMethodField('check_show')

    def check_show(self,obj):     
        if obj.show == False:
            obj.identifier = None
            obj.id = None
            obj.title = None
            obj.author_name = None
            obj.featured = None
            obj.content_body = None
            obj.thumbnail_image = None
            obj.date_to_show = None
            return False

        elif obj.show == True:
            return True
    class Meta:
        model = models.Post
        fields = ('show_bool','id','title','author_name','thumbnail_image','content_body','date_to_show')


class CommentSerializer(serializers.ModelSerializer):
    blog_post_id = serializers.SerializerMethodField('get_blog_id')

    def get_blog_id(self,obj):
        return obj.post.id

    class Meta:
        model = models.Comment
        fields = ('id','parent_id','blog_post_id','data')