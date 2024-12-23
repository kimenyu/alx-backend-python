from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Message, Conversation

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def create(self, validated_data):
        sender = self.context['request'].user
        message = Message.objects.create(sender=sender, **validated_data)
        return message


class ConversationListSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'last_message', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        participants_data = self.context['request'].data.get('participants', [])
        conversation = Conversation.objects.create()
        conversation.participants.set(participants_data)
        return conversation

    def update(self, instance, validated_data):
        participants_data = self.context['request'].data.get('participants', [])
        instance.participants.set(participants_data)
        return instance