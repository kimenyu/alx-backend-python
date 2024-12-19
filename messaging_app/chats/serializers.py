from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Override create method to properly handle password hashing."""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = CustomUserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'conversation',
                 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model with nested messages."""
    participants = CustomUserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids',
                 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        """Override create method to handle participant IDs."""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        if participant_ids:
            participants = CustomUser.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation

# Serializer for limited user data (useful for nested relationships where you don't need full user details)
class BasicUserSerializer(serializers.ModelSerializer):
    """Simplified serializer for nested user representations."""
    
    class Meta:
        model = CustomUser
        fields = ['user_id', 'first_name', 'last_name', 'email']
        read_only_fields = ['user_id']