from rest_framework.pagination import PageNumberPagination

class CustomMessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
