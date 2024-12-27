from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Allow access only to the owner of a conversation or message.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming `obj` can be a Message or Conversation with `participants`
        return request.user in obj.conversation.participants.all()


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to send, view,
    update, or delete messages.
    """
    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only participants of the conversation
        # Assuming `obj` is a message and has a `conversation` attribute with `participants`
        return request.user in obj.conversation.participants.all()
