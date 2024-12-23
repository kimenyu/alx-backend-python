from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Initialize the parent router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Initialize the nested router for messages
messages_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# URL patterns for the chat app
urlpatterns = [
    path('', include(router.urls)),
    path('', include(messages_router.urls)),
]