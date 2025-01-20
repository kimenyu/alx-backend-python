from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User, Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        request.data['sender'] = sender.id  # Ensure sender is set properly
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Optionally filter messages by conversation ID (if provided)
        conversation_id = request.query_params.get('conversation_id', None)
        if conversation_id:
            queryset = Message.objects.filter(conversation__conversation_id=conversation_id)
        else:
            queryset = Message.objects.filter(sender=request.user)  # Only messages sent by the logged-in user
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if request.user.id not in participants:
            participants.append(request.user.id)  # Add logged-in user if not already present
        request.data['participants'] = participants
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Filter conversations by the logged-in user
        queryset = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)
