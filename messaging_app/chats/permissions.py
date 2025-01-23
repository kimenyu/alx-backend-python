from rest_framework.permissions import BasePermission

class IsParticipantOrSender(BasePermission):
    """
    Custom permission to allow users to access their own conversations and messages.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # Check if it's a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'sender'):  # Check if it's a Message
            return request.user == obj.sender or request.user in obj.conversation.participants.all()
        return False
