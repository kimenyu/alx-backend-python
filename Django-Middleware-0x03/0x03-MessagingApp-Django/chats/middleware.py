import datetime
import logging
from django.http import HttpResponseForbidden
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up the logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        # Extract user and request path
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"
        
        # Log the request
        logging.info(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_reponse):
        self.get_response = get_reponse

    def __call__(self, request):
        current = datetime.datetime.now().hour

        if current < 9 or current >= 18:
            return HttpResponseForbidden(
                "Access to the messaging app outside 9 AM to 6 PM"
            )
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_tracker = {}

    def __call__(self, request):
        if request.method == "POST" and "/messages/" in request.path:
            ip = self.get_client_ip(request)
            current_time = datetime.now()

            if ip not in self.requests_tracker:
                self.requests_tracker[ip] = {"count": 1, "start_time": current_time}
            else:
                data = self.requests_tracker[ip]
                elapsed_time = current_time - data["start_time"]


                if elapsed_time > datetime.timedelta(minutes=1):
                    self.requests_tracker[ip] = {"count": 1, "start_time": current_time}
                else:
                    # Enforce rate limiting
                    if data["count"] >= 5:
                        return JsonResponse(
                            {"error": "Rate limit exceeded. Try again later."},
                            status=429,
                        )
                    self.requests_tracker[ip]["count"] += 1

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """
        Retrieve the client's IP address from the request headers.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

class RolePermissionMiddleware:
    """
    Middleware to restrict access based on user roles (admin or moderator).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ["/admin/", "/moderator/"]

        if any(path in request.path for path in protected_paths):
            user = request.user

            if not user.is_authenticated or user.role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Access forbidden: Admin or Moderator role required."},
                    status=403,
                )

        response = self.get_response(request)
        return response