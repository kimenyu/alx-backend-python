from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    USER_ROLES = [('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')]
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=128)  # For storing hashed password
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    role = models.CharField(max_length=5, choices=USER_ROLES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    class Meta:
        indexes = [models.Index(fields=['email'])]

class Conversation(models.Model):
    """Model to represent conversations between users"""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants_id = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f"Conversation {self.conversation_id} - {self.participants_id.count()} participants"

class Message(models.Model):
    """Model to represent individual messages within a conversation"""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['sent_at']), models.Index(fields=['sender_id'])]
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender_id.email} at {self.sent_at}"