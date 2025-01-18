import logging
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        self.logger = logging.getLogger('django')
        handler = logging.FileHandler('request_logs.log')  # Log to a file
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Get the user making the request (or 'Anonymous' if not logged in)
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server time (24-hour format)
        current_hour = datetime.now().hour
        
        # Define restricted hours (outside 9 AM to 6 PM)
        if current_hour < 9 or current_hour >= 18:
            # Check if the user is trying to access the messaging app (e.g., /chat/)
            if request.path.startswith('/chat/'):
                return HttpResponseForbidden("Access to the messaging app is restricted outside 9 AM to 6 PM.")
        
        # Proceed with the request if it's not restricted
        response = self.get_response(request)
        return response



class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track IP addresses and their request timestamps
        self.ip_requests = {}

    def __call__(self, request):
        # Only track POST requests to the chat endpoint
        if request.method == 'POST' and request.path.startswith('/chat/'):
            # Get the user's IP address
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize or update the request log for this IP
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []
            
            # Remove timestamps older than 1 minute
            self.ip_requests[ip] = [
                timestamp for timestamp in self.ip_requests[ip]
                if now - timestamp <= timedelta(minutes=1)
            ]
            
            # Check the number of requests in the last 1 minute
            if len(self.ip_requests[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            # Add the current request timestamp
            self.ip_requests[ip].append(now)

        # Proceed with the request if within limits
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract the IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted paths
        restricted_paths = ['/admin-action/']

        # Check if the user is trying to access a restricted path
        if any(request.path.startswith(path) for path in restricted_paths):
            # Check if the user is authenticated and has the correct role
            user = request.user
            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this action.")
        
        # Proceed with the request
        response = self.get_response(request)
        return response
