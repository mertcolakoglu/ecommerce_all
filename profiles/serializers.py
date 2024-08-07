from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_name_surname', 'profile_image', 'email', 'phone_number', 'address', 'is_supplier']
        read_only_fields = ['email']