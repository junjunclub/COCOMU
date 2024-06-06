from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['ott', 'genre1', 'genre2', 'genre3']

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=10)
    nickname = serializers.CharField(max_length=12)
    birth = serializers.DateField()

    def save(self, request):
        user = super().save(request)
        user.name = self.data.get('name')
        user.nickname = self.data.get('nickname')
        user.birth = self.data.get('birth')
        user.save()
        return user
    
class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})
    
