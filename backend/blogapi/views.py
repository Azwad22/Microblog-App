from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,permissions, viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)    
    
    
    
class UserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class PostListView(ListAPIView):
    queryset = Post.objects.order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    
class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.order_by('-created_at')
    serializer_class = PostSerializer
    lookup_field= 'pid'
    permission_classes = (permissions.AllowAny,)
    
class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field= 'pid'
    permission_classes = (permissions.AllowAny,)
    
class VoteDetailView(ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)
    
    
