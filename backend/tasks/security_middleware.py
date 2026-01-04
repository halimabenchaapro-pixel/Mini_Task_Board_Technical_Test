"""
Security middleware to prevent common cyber attacks
Protects against: XSS, Clickjacking, MIME sniffing, SQL injection patterns
"""
import re
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to prevent common attacks:
    - XSS attacks
    - Clickjacking
    - MIME sniffing
    - Information disclosure
    """

    def process_response(self, request, response):
        # Prevent XSS attacks
        response['X-XSS-Protection'] = '1; mode=block'

        # Prevent clickjacking attacks
        response['X-Frame-Options'] = 'DENY'

        # Prevent MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Content Security Policy (basic)
        response['Content-Security-Policy'] = "default-src 'self'"

        # Remove server header to prevent information disclosure
        if 'Server' in response:
            del response['Server']

        # HSTS header (for HTTPS in production)
        # Uncomment when using HTTPS
        # response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response


class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """
    Detect and block potential SQL injection attempts
    Note: Django ORM already protects against SQL injection,
    but this adds an extra layer for raw queries
    """

    # Common SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bSELECT\b.*\bFROM\b.*\bWHERE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bUPDATE\b.*\bSET\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bEXEC\b.*\()",
        r"(';.*--)",
        r"(\bOR\b.*=.*)",
        r"(1=1)",
        r"('.*OR.*'.*=.*')",
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.sql_pattern = re.compile(
            '|'.join(self.SQL_INJECTION_PATTERNS),
            re.IGNORECASE
        )

    def __call__(self, request):
        # Check query parameters for SQL injection patterns
        if self._contains_sql_injection(request.GET):
            logger.warning(
                f"Potential SQL injection attempt detected from {request.META.get('REMOTE_ADDR')}: {request.GET}"
            )
            return JsonResponse(
                {'error': 'Invalid request parameters'},
                status=400
            )

        # Check POST data for SQL injection patterns
        if request.method == 'POST' and hasattr(request, 'POST'):
            if self._contains_sql_injection(request.POST):
                logger.warning(
                    f"Potential SQL injection attempt detected from {request.META.get('REMOTE_ADDR')}: {request.POST}"
                )
                return JsonResponse(
                    {'error': 'Invalid request data'},
                    status=400
                )

        response = self.get_response(request)
        return response

    def _contains_sql_injection(self, data):
        """Check if data contains potential SQL injection patterns"""
        for key, value in data.items():
            if isinstance(value, str) and self.sql_pattern.search(value):
                return True
        return False


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log all API requests for security auditing
    Helps detect suspicious patterns and attack attempts
    """

    def process_request(self, request):
        if request.path.startswith('/api/'):
            logger.info(
                f"API Request: {request.method} {request.path} "
                f"from {request.META.get('REMOTE_ADDR')} "
                f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
            )
        return None

    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            logger.info(
                f"API Response: {request.method} {request.path} "
                f"Status: {response.status_code}"
            )
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple rate limiting to prevent brute force attacks
    Limits requests per IP address
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts: {ip: [(timestamp, count), ...]}
        self.request_counts = {}
        self.max_requests = 100  # Max requests per window
        self.window_seconds = 60  # Time window in seconds

    def __call__(self, request):
        import time

        if not request.path.startswith('/api/'):
            return self.get_response(request)

        ip = self._get_client_ip(request)
        current_time = time.time()

        # Clean old entries
        if ip in self.request_counts:
            self.request_counts[ip] = [
                (ts, count) for ts, count in self.request_counts[ip]
                if current_time - ts < self.window_seconds
            ]

        # Count requests in current window
        if ip not in self.request_counts:
            self.request_counts[ip] = []

        total_requests = sum(count for _, count in self.request_counts[ip])

        if total_requests >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return JsonResponse(
                {
                    'error': 'Too many requests. Please try again later.',
                    'retry_after': self.window_seconds
                },
                status=429
            )

        # Add current request
        self.request_counts[ip].append((current_time, 1))

        response = self.get_response(request)

        # Add rate limit headers
        response['X-RateLimit-Limit'] = str(self.max_requests)
        response['X-RateLimit-Remaining'] = str(self.max_requests - total_requests - 1)

        return response

    def _get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class XSSProtectionMiddleware(MiddlewareMixin):
    """
    Detect and sanitize potential XSS attacks in request data
    """

    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<embed[^>]*>',
        r'<object[^>]*>',
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.xss_pattern = re.compile(
            '|'.join(self.XSS_PATTERNS),
            re.IGNORECASE | re.DOTALL
        )

    def __call__(self, request):
        # Check for XSS in query parameters
        if self._contains_xss(request.GET):
            logger.warning(
                f"Potential XSS attempt detected from {request.META.get('REMOTE_ADDR')}"
            )
            return JsonResponse(
                {'error': 'Invalid request parameters'},
                status=400
            )

        response = self.get_response(request)
        return response

    def _contains_xss(self, data):
        """Check if data contains potential XSS patterns"""
        for key, value in data.items():
            if isinstance(value, str) and self.xss_pattern.search(value):
                return True
        return False
