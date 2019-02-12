from django.shortcuts import render

from rest_framework import viewsets

from api.models import Company, User, Job
from api.serializers import CompanyReadSerializer, CompanyWriteSerializer, UserReadSerializer, UserWriteSerializer, JobReadSerializer, JobWriteSerializer
# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD']:
            return CompanyReadSerializer
        else:
            return CompanyWriteSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD']:
            return UserReadSerializer
        else:
            return UserWriteSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD']:
            return JobReadSerializer
        else:
            return JobWriteSerializer