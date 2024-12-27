import django_filters
from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """
    Filter messages by sender, recipient, and date range.
    """
    sender = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    recipient = filters.CharFilter(field_name='conversation__participants__username', lookup_expr='icontains')
    start_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']
