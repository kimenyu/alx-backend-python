from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Derived field

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']
        read_only_fields = ['user_id', 'created_at']

    def validate_email(self, value):
        if "spam" in value:  # Example of a validation check
            raise serializers.ValidationError("Invalid email containing 'spam'.")
        return value


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # Derived field to include sender's full name

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'conversation']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()  # Custom method to handle nested relationships
    messages = MessageSerializer(many=True, read_only=True,)  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_participants(self, obj):
        return [f"{participant.first_name} {participant.last_name}" for participant in obj.participants.all()]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'phone_number', 'role']

    def create(self, validated_data):
        # Create a new user with the provided data
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number'),
            role=validated_data['role'],
        )
        # Set the password securely
        user.set_password(validated_data['password'])
        user.save()
        return user