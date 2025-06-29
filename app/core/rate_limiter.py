import time
import functools
from typing import Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import threading

from fastapi import Request, HTTPException

from app import setting


class RateLimiter:
    """
    Custom rate limiter implementation using sliding window approach.
    Thread-safe implementation for handling concurrent requests.
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed per window
            window_seconds: Time window in seconds (default: 1 hour)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str) -> Tuple[bool, Dict]:
        """
        Check if request is allowed for the given identifier.

        Args:
            identifier: Unique identifier (e.g., IP address, organization ID)

        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        current_time = time.time()

        with self.lock:
            # Clean old requests outside the window
            self._cleanup_old_requests(identifier, current_time)

            request_count = len(self.requests[identifier])

            # Check if request is allowed
            if request_count >= self.max_requests:
                reset_time = datetime.fromtimestamp(
                    self.requests[identifier][0] + self.window_seconds
                )
                return False, {
                    'requests_remaining': 0,
                    'reset_time': reset_time,
                    'limit': self.max_requests
                }

            # Add current request
            self.requests[identifier].append(current_time)

            # Calculate reset time (when oldest request expires)
            reset_time = datetime.fromtimestamp(
                self.requests[identifier][0] + self.window_seconds
            ) if self.requests[identifier] else datetime.now() + timedelta(seconds=self.window_seconds)

            return True, {
                'requests_remaining': self.max_requests - (request_count + 1),
                'reset_time': reset_time,
                'limit': self.max_requests
            }

    def _cleanup_old_requests(self, identifier: str, current_time: float):
        """Remove requests that are outside the current window."""
        cutoff_time = current_time - self.window_seconds
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff_time
        ]

    def get_stats(self, identifier: str) -> Dict:
        """Get current rate limit statistics for an identifier."""
        current_time = time.time()

        with self.lock:
            self._cleanup_old_requests(identifier, current_time)
            request_count = len(self.requests[identifier])

            reset_time = datetime.fromtimestamp(
                self.requests[identifier][0] + self.window_seconds
            ) if self.requests[identifier] else datetime.now() + timedelta(seconds=self.window_seconds)

            return {
                'requests_remaining': max(0, self.max_requests - request_count),
                'reset_time': reset_time,
                'limit': self.max_requests,
                'current_requests': request_count
            }

    def reset(self, identifier: str):
        """Reset rate limit for a specific identifier."""
        with self.lock:
            if identifier in self.requests:
                del self.requests[identifier]

    def reset_all(self):
        """Reset rate limits for all identifiers."""
        with self.lock:
            self.requests.clear()


SEARCH_RATE_LIMITER = RateLimiter(
    max_requests=setting.SEARCH_RATE_LIMIT,
    window_seconds=setting.RATE_LIMIT_WINDOW
)
GENERAL_RATE_LIMITER = RateLimiter(
    max_requests=setting.GENERAL_RATE_LIMIT,
    window_seconds=setting.RATE_LIMIT_WINDOW
)


def rate_limit_decorator(rate_limiter, identifier_func):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            if request is None:
                raise RuntimeError('Request object not found in endpoint arguments')

            identifier = identifier_func(request)
            allowed, info = rate_limiter.is_allowed(identifier)
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=f'Rate limit exceeded. Try again at {info['reset_time']}.'
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_ip_identifier(request: Request):
    return request.client.host
