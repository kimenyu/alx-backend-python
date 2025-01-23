from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOfConversation, IsSenderOfMessage
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth import CustomTokenObtainPairSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    permission_classes = [IsAuthenticated, IsOwnerOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    def get_queryset(self):
        # Return only conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle creating a new conversation.
        """
        participants_ids = request.data.get('participants')
        if not participants_ids:
            return Response(
                {"error": "Participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(user_id__in=participants_ids)
        if not participants.exists():
            return Response(
                {"error": "Invalid participant IDs provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    permission_classes = [IsAuthenticated, IsSenderOfMessage]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']

    def get_queryset(self):
        # Return only messages in conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle sending a new message.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response(
                {"error": "sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )


class SignupView(APIView):
    """
    Endpoint for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer