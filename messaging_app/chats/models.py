from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID primary key
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)  # nullable phone number
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID primary key
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Foreign key to User
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.sender.username} - {self.message_body[:50]}...'  # Display part of the message

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID primary key
    participants = models.ManyToManyField(User, related_name='conversations')  # Many to Many relationship with User
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Conversation {self.conversation_id}'
