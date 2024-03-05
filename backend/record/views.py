from rest_framework import viewsets
from record.serializers import UserSerializer, DailyRecordSerializer, LoginAccessSerializer
from .models import User, DailyRecord, LoginAccess

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DailyRecordViewSet(viewsets.ModelViewSet):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer

class LoginAccessViewSet(viewsets.ModelViewSet):
    queryset = LoginAccess.objects.all()
    serializer_class = LoginAccessSerializer