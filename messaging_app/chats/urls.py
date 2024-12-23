from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# URL patterns for the chat app
urlpatterns = [
    path('', include(router.urls)),
]