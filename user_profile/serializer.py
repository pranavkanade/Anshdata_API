from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from core.models import Producer, Consumer


class UserSerializer(ModelSerializer):
    """
    Serialize User model
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'is_producer')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}    # one can add min_length here
        }

    # following function needs to be explicitly defined
    def create(self, validated_data):
        """
        Create a new user with encrypted password and return the user
        """
        return get_user_model().objects.create_user(**validated_data)


class UserDetailSerializer(ModelSerializer):
    """
    Serialize User model
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_producer', 'date_joined')
        read_only_fields = ('id',)


class ProducerSerializer(ModelSerializer):
    """
    Serialize a producer object
    """
    class Meta:
        model = Producer
        fields = ('user', 'company_name')


class ProducerDetailedSerializer(ProducerSerializer):
    user = UserDetailSerializer(many=False, read_only=True)


class ConsumerSerializer(ModelSerializer):
    class Meta:
        model = Consumer
        fields = ('user', 'date_of_birth')


class ConsumerDetailedSerializer(ConsumerSerializer):
    user = UserDetailSerializer(many=False, read_only=True)
