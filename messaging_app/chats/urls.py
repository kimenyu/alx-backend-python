from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, UserCreateView

# Create a regular router for the conversations and messages
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='conversation-messages')  # Regular route for messages

# Create a regular router for the user-related endpoints
auth_router = routers.DefaultRouter()
auth_router.register(r'users', UserCreateView, basename='users')

# Define the main API URL patterns
main_api_urlpatterns = [
    path('', include(router.urls)),
]

# Define the auth API URL patterns
auth_api_urlpatterns = [
    path('', include(auth_router.urls)),
]
