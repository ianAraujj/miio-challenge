from django.shortcuts import render
from user.utils import is_authenticated

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import RegularPlan
from user.utils import is_authenticated
from .serializers import RegularPlanSerializer
from django.shortcuts import get_object_or_404

# Create your views here.


class RegularPlanView(ModelViewSet):

	parser_classes = (JSONParser,)
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = RegularPlanSerializer

	def get_queryset(self):
		user = is_authenticated(self.request)
		publish = self.request.query_params.get("publish", None)
		
		if publish != None:
			queryset = RegularPlan.objects.filter(publish=True)
		else:
			queryset = RegularPlan.objects.filter(owner=user)
		return queryset



	def create(self, request):
		user = is_authenticated(request)
		
		regular_plan_data = request.data

		serializer = RegularPlanSerializer(data=regular_plan_data)
		serializer.is_valid(raise_exception=True)
		
		regular_plan_response = serializer.create(serializer.validated_data)		
		regular_plan_response = RegularPlanSerializer(regular_plan_response)

		return Response(data=regular_plan_response.data, status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk=None):
		pass

	def update(self, request, pk=None):
		user = is_authenticated(request)

		instance = get_object_or_404(RegularPlan, id=pk)

		serializer = self.serializer_class(instance, data=request.data)

		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(data=serializer.data, status=status.HTTP_201_CREATED)