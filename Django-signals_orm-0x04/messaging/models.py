from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  edited = models.BooleanField(default=False)
  parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
  read = models.BooleanField(default=False)

  objects = models.Manager()
  unread = UnreadMessagesManager()

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='edited_message')
