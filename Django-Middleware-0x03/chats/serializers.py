from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender_id.first_name', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_name', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
        
    def create(self, validated_data):
        sender_data = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_data['user_id'])
        return Message.objects.create(sender_id=sender, **validated_data)
    
    def update(self, instance, validated_data):
        # Update the Message instance
        instance = super().update(instance, validated_data)
        return instance
    
    #get all messages
    def get_messages(self):
        return Message.objects.all()
    
    


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()


    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        # Extract nested data
        participants_data = validated_data.pop('participants_id', [])
        messages_data = validated_data.pop('messages', [])

        # Create the Conversation
        conversation = Conversation.objects.create(**validated_data)

        # Add participants
        participants = [User.objects.get(user_id=participant['user_id']) for participant in participants_data]
        conversation.participants_id.set(participants)

        # Add messages
        for message_data in messages_data:
            sender_data = message_data.pop('sender_id')
            sender = User.objects.get(user_id=sender_data['user_id'])
            Message.objects.create(conversation=conversation, sender_id=sender, **message_data)

        return conversation

    def update(self, instance, validated_data):
        # Extract nested data
        participants_data = validated_data.pop('participants_id', None)
        messages_data = validated_data.pop('messages', None)

        # Update the Conversation instance
        instance = super().update(instance, validated_data)

        # Update participants
        if participants_data is not None:
            participants = [User.objects.get(user_id=participant['user_id']) for participant in participants_data]
            instance.participants_id.set(participants)

        # Update messages (assumes messages are not updated in bulk but new ones can be added)
        if messages_data is not None:
            for message_data in messages_data:
                sender_data = message_data.pop('sender_id')
                sender = User.objects.get(user_id=sender_data['user_id'])
                Message.objects.create(conversation=instance, sender_id=sender, **message_data)

        return instance
    
    #validate atleast 2 participants
    def validate(self, data):
        if len(data['participants_id']) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data
    
    def get_messages(self, obj):
        """
        Custom method to retrieve messages in the conversation.
        """
        messages = obj.messages.all()  # `related_name='messages'` used in the Message model
        return MessageSerializer(messages, many=True).data