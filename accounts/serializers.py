from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='userprofile.profile_image', required=False)

    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'profile_image']
