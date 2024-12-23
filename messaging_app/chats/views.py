from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling conversation operations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get conversations where the current user is a participant.
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation and add participants.
        """
        # Add the current user to participants if not included
        participant_ids = request.data.get('participant_ids', [])
        if str(request.user.user_id) not in participant_ids:
            participant_ids.append(str(request.user.user_id))
        
        # Update request data with modified participant_ids
        request.data['participant_ids'] = participant_ids
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def add_participants(self, request, pk=None):
        """
        Add participants to an existing conversation.
        """
        conversation = self.get_object()
        participant_ids = request.data.get('participant_ids', [])
        
        if not participant_ids:
            return Response(
                {"error": "No participant IDs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add new participants
        conversation.participants.add(*participant_ids)
        serializer = self.get_serializer(conversation)
        
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_participants(self, request, pk=None):
        """
        Remove participants from a conversation.
        """
        conversation = self.get_object()
        participant_ids = request.data.get('participant_ids', [])
        
        if not participant_ids:
            return Response(
                {"error": "No participant IDs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Can't remove yourself if you're the only participant
        remaining_count = conversation.participants.exclude(
            user_id__in=participant_ids
        ).count()
        
        if remaining_count < 2:
            return Response(
                {"error": "Conversation must have at least 2 participants"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove participants
        conversation.participants.remove(*participant_ids)
        serializer = self.get_serializer(conversation)
        
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling message operations.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sent_at', 'sender']
    search_fields = ['content']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """
        Get messages for a specific conversation.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id
            ).order_by('-sent_at')
        return Message.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation.
        """
        # Set the sender as the current user
        request.data['sender_id'] = request.user.user_id
        
        # Set the conversation from the URL
        conversation_id = self.kwargs.get('conversation_pk')
        request.data['conversation'] = conversation_id
        
        # Verify user is a participant in the conversation
        conversation = Conversation.objects.filter(
            conversation_id=conversation_id,
            participants=request.user
        ).first()
        
        if not conversation:
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)