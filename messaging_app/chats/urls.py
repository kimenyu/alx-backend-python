from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ConversationViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Include the router's URLs in your app's URL configuration
urlpatterns = [
    path('api/', include(router.urls)),  # All your API endpoints will be prefixed with '/api/'
]
