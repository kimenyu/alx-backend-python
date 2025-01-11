from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import filters


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling conversation operations.
    Supports: list, create, retrieve, update, delete
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter conversations to only show those where the current user is a participant
        """
        return self.queryset.filter(participants_id=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new conversation and automatically add the current user as a participant
        """
        conversation = serializer.save()
        conversation.participants_id.add(self.request.user)
        return conversation

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participants
        """
        # Ensure the request data includes participants
        if 'participants_id' not in request.data:
            return Response(
                {"error": "participants_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add current user to participants if not already included
        participants = request.data.get('participants_id', [])
        if request.user.user_id not in participants:
            participants.append(request.user.user_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling message operations.
    Supports: list, create, retrieve
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages to only show those from conversations where the user is a participant
        """
        return self.queryset.filter(
            conversation__participants_id=self.request.user
        )

    def perform_create(self, serializer):
        """
        Create a new message, automatically setting the sender as the current user
        """
        serializer.save(sender_id=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation
        """
        # Validate that the conversation exists and user is a participant
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants_id=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found or you're not a participant"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )