import logging
from datetime import datetime
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
