import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter for filtering messages by sender and by a date range.
    """
    participant_id = django_filters.UUIDFilter(field_name='sender_id__user_id', lookup_expr='exact')
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant_id', 'start_date', 'end_date']
