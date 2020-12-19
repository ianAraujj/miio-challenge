from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .utils import is_authenticated, generate_token_to_user
from .serializers import UserSerializer
from .exceptions import NonAuthorized
# Create your views here.

class UserRegisterView(ModelViewSet):
	parser_classes = (JSONParser,)
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		serializer = self.serializer_class(data=request.data)
		
		status_code = status.HTTP_201_CREATED
		response_data = {}
	
		serializer.is_valid(raise_exception=True)
		new_user = serializer.create()

		new_user_serializer = self.serializer_class(new_user)

		return Response(data=new_user_serializer.data, status=status_code)

class UserLoginView(ModelViewSet):
	parser_classes = (JSONParser,)
	serializer_class = UserSerializer
	permission_classes = [AllowAny]

	def create(self, request):
		user = authenticate(username=request.data['username'], password=request.data['password'])
		
		if user != None:
			serializer = UserSerializer(user, many=False)
			token = generate_token_to_user(user)
			
			response_data = {}
			response_data['user'] = serializer.data
			response_data['token'] = token
		else:
			raise NonAuthorized("Username or password are incorrect")

		return Response(data=response_data, status=status.HTTP_200_OK)
