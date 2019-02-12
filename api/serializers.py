from rest_framework import serializers

from api.models import Company, User, Job

class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserReadSerializer(serializers.ModelSerializer):
    workfor = CompanyReadSerializer

    class Meta:
        model = User
        fields = '__all__'

class JobReadSerializer(serializers.ModelSerializer):
    workfor = CompanyReadSerializer

    class Meta:
        model = Job
        fields = '__all__'

class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class JobWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'