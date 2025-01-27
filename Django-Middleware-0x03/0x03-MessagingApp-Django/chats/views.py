from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationFilter(filters.FilterSet):
    # You can filter by participant ID or other fields
    participant_id = filters.UUIDFilter(field_name="participants__id", lookup_expr="exact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Conversation
        fields = ['participant_id', 'created_at']

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter

    def create(self, request, *args, **kwargs):
        """Create a new conversation."""
        # Creating a new conversation instance based on incoming data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save and return the created conversation
            conversation = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MessageFilter(filters.FilterSet):
    sender_id = filters.UUIDFilter(field_name="sender__id", lookup_expr="exact")
    conversation_id = filters.UUIDFilter(field_name="conversation__id", lookup_expr="exact")
    sent_at = filters.DateFromToRangeFilter(field_name="sent_at")

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id', 'sent_at']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def create(self, request, *args, **kwargs):
        """Send a new message to an existing conversation."""
        # Ensure conversation exists before creating a message
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Proceed to create the message
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


