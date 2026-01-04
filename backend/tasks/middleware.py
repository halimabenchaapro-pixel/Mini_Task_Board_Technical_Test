from django.http import JsonResponse
from django.conf import settings


class APIKeyMiddleware:
    """Middleware to check API key in request headers"""

    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that don't require authentication
        self.exempt_paths = [
            '/admin/',
        ]

    def __call__(self, request):
        # Check if path is exempt
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        # Check if this is an API request
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-KEY')

            if not api_key:
                return JsonResponse(
                    {'error': 'API key is required. Please provide X-API-KEY header.'},
                    status=401
                )

            if api_key != settings.API_KEY:
                return JsonResponse(
                    {'error': 'Invalid API key.'},
                    status=403
                )

        response = self.get_response(request)
        return response
