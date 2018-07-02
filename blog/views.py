from django.shortcuts import render
from rest_framework import viewsets, generics
from blog import serializers
from blog import models
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializers
    lookup_field = 'id'
    http_method_names = ['get']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    lookup_field = 'id'
    http_method_names = ['get','post']