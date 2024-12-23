from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Message, Conversation

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested UserSerializer for the sender

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested UserSerializer for participants
    messages = MessageSerializer(many=True, read_only=True)  # Nested MessageSerializer for messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_participant_names(self, obj):
        return [f"{participant.first_name} {participant.last_name}".strip() for participant in obj.participants.all()]
    
    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants")
        return value

    