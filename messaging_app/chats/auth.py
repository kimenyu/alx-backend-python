from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def get_tokens_for_user(user):
    """
    Generate JWT tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to include user_id in the token response.
    """
    def validate(self, attrs):
        # Call the parent validate method to get the default response data
        data = super().validate(attrs)

        # Add the user's ID to the response
        data['user_id'] = str(self.user.user_id)  # Ensure user_id is returned
        return data