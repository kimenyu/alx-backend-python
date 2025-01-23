from rest_framework.permissions import BasePermission

class IsOwnerOfConversation(BasePermission):
    """
    Custom permission to allow only owners (participants) to view a conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is a participant in the conversation
        return request.user in obj.participants.all()


class IsSenderOfMessage(BasePermission):
    """
    Custom permission to allow only the sender to view or modify a message.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the sender of the message
        return request.user == obj.sender