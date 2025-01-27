from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """
    Filter messages by sender, time range, or conversation.
    """
    sender = filters.CharFilter(field_name="sender__user_id", lookup_expr="exact")
    created_at_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    conversation = filters.CharFilter(field_name="conversation__conversation_id", lookup_expr="exact")

    class Meta:
        model = Message
        fields = ['sender', 'created_at_after', 'created_at_before', 'conversation']
