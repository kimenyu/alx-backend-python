from rest_framework import viewsets
from .models import Notification, Message
from django.shortcuts import get_object_or_404
from .serializers import NotificationSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.shortcuts import render

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete_user(self, request):
        sender=request.user
        sender.delete()
        return Response({"message": "Your account has been deleted successfully."}, status=status.HTTP_200_OK)
    

@cache_page(60)
class ThreadedConversationView(APIView):
    def get(self, request, conversation_id):
        messages = Message.objects.filter(parent_message=None, receiver_id=conversation_id).prefetch_related(
            'replies__replies',
        ).select_related('sender', 'receiver')

        data = [
            {
                "id": message.id,
                "content": message.content,
                "timestamp": message.timestamp,
                "replies": self.get_replies(message)
            }
            for message in messages
        ]
        return Response(data, status=status.HTTP_200_OK)

    def get_replies(self, message):
        return [
            {
                "id": reply.id,
                "content": reply.content,
                "timestamp": reply.timestamp,
                "replies": self.get_replies(reply)
            }
            for reply in message.replies.all()
        ]
    
class UnreadMessagesView(APIView):
    def get(self, request):
        user = request.user
        unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp')

        data = [
            {
                "id": message.id,
                "sender": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in unread_messages
        ]
        return Response(data, status=status.HTTP_200_OK)
    