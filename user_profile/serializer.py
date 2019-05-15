from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from core.models.profile import Social, Profile


class SocialSerializer(ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(ModelSerializer):
    """
    Serialize User model
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'profile', 'social')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}    # one can add min_length here
        }

    # following function needs to be explicitly defined as we have defined manager explicitly
    def create(self, validated_data):
        print("[create] : UserSerializer")
        """
        Create a new user with encrypted password and return the user
        """
        return get_user_model().objects.create_user(**validated_data)


class UserDetailedSerializer(ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    social = SocialSerializer(many=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'profile', 'social')
