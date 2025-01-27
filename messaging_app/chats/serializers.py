from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """
        Ensure password and confirm_password match.
        """
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """
        Overriding the create method to hash the password.
        """
        password = validated_data.pop('password')
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        # Use the create_user method to ensure password hashing
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
        )
        
        user.set_password(password)
        user.save()

        user.groups.set(groups)
        user.user_permissions.set(user_permissions)

        return user

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle password hashing.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_fullname(self, obj):
        """
        Retrieve the full name of the message sender.
        """
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'
