from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    """
    Serialize User model
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
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
