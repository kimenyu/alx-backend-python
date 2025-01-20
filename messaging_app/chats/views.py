from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['conversation']  # Filter by conversation
    ordering_fields = ['sent_at']  # Allow ordering by sent_at (to get most recent first)
    ordering = ['sent_at']  # Default ordering by sent_at
    
    def create(self, request, *args, **kwargs):
        sender = request.user
        request.data['sender'] = sender.id  # Ensure sender is set properly
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        conversation_id = request.query_params.get('conversation_id', None)
        if conversation_id:
            queryset = Message.objects.filter(conversation__conversation_id=conversation_id)
        else:
            queryset = Message.objects.filter(sender=request.user)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if request.user.id not in participants:
            participants.append(request.user.id)
        request.data['participants'] = participants
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)
