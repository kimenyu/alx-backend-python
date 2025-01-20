from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import MessageViewSet, ConversationViewSet

# Create a default router and register the ConversationViewSet
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router to register MessageViewSet under the ConversationViewSet
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Include the routes from the router and the nested router
urlpatterns = [
    path('api/', include(router.urls)),  # Include the default router (for conversations)
    path('api/', include(nested_router.urls)),  # Include the nested router (for messages under conversations)
]
