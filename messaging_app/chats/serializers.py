from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = CustomUserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
