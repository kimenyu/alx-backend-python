from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""
    full_name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 
                 'full_name', 'phone_number', 'role', 'role_display', 'created_at']
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

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
    formatted_timestamp = serializers.SerializerMethodField()
    message_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'conversation',
                 'message_body', 'message_preview', 'sent_at', 'formatted_timestamp']
        read_only_fields = ['message_id', 'sent_at']

    def get_formatted_timestamp(self, obj):
        return obj.sent_at.strftime("%B %d, %Y %H:%M:%S")

    def get_message_preview(self, obj):
        max_length = 50
        return f"{obj.message_body[:max_length]}..." if len(obj.message_body) > max_length else obj.message_body

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model with nested messages."""
    participants = CustomUserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()
    conversation_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids',
                 'messages', 'last_message', 'message_count', 
                 'conversation_title', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_conversation_title(self, obj):
        participants = obj.participants.all()
        if participants.count() == 2:
            # For one-on-one conversations
            return " & ".join([f"{p.first_name}" for p in participants])
        else:
            # For group conversations
            return f"Group Chat ({participants.count()} participants)"

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value

    def create(self, validated_data):
        """Override create method to handle participant IDs."""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        if participant_ids:
            participants = CustomUser.objects.filter(user_id__in=participant_ids)
            if participants.count() != len(participant_ids):
                raise serializers.ValidationError("One or more participant IDs are invalid.")
            conversation.participants.set(participants)
        
        return conversation

class BasicUserSerializer(serializers.ModelSerializer):
    """Simplified serializer for nested user representations."""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['user_id', 'full_name', 'email']
        read_only_fields = ['user_id']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"