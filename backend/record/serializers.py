from rest_framework import serializers
from .models import User, DailyRecord, LoginAccess

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecord
        fields = '__all__'

class LoginAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAccess
        fields = '__all__'