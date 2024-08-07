from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from profiles.serializers import ProfileSerializer

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'profile')