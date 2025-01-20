from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        # We don't include the password here, but you can handle it separately if needed


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.EmailField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id',  'sender_name', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Message body cannot be empty')
        return value

    # Method to create a new message
    def create(self, validated_data):
        sender = validated_data.pop('sender')
        message = Message.objects.create(sender=sender, **validated_data)
        return message

    # Method to update a message
    def update(self, instance, validated_data):
        instance.message_body = validated_data.get('message_body', instance.message_body)
        instance.save()
        return instance


class ConversationSerializer(serializers.ModelSerializer):
    participants_emails= serializers.EmailField(source='participants.email', read_only=True)
    messages = MessageSerializer(many=True)
    message_count = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_emails', 'messages', 'message_count', 'participants_count', 'created_at']

    # Validate that the participants list has more than one user
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('A conversation must have more than one participant')
        return value

    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_partcipants_count(self, obj):
        return obj.participants.count()
