from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

class User(AbstractUser):
  class Meta:
    app_label = 'chats'
  user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  first_name = models.CharField(max_length=100, null=False)
  last_name = models.CharField(max_length=100, null=False)
  email = models.EmailField(unique=True, null=False, db_index=True)
  password_hash = models.CharField(max_length=100, null=False)
  phone_number = models.CharField(max_length=100, null=True)
  role = models.CharField(max_length=100, choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')], null=False)
  created_at = models.DateTimeField(auto_now=True)
  user_permissions = models.ManyToManyField(
    Permission,
    blank=True,
    related_name='chat_user_permissions'  # Change related_name to avoid clashes
  )
    
  groups = models.ManyToManyField(
    Group,
    blank=True,
    related_name='chat_user_groups'  # Change related_name to avoid clashes
  )


class Conversation(models.Model):
  conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
  participants = models.ManyToManyField(User, related_name='conversations')
  created_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)