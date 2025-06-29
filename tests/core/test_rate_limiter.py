import time
from fastapi import Request
from starlette.responses import JSONResponse

from app.core.rate_limiter import RateLimiter, rate_limit_decorator, get_ip_identifier

from app.main import app

test_limiter = RateLimiter(max_requests=3, window_seconds=2)


@app.get('/limited')
@rate_limit_decorator(test_limiter, get_ip_identifier)
def limited_endpoint(request: Request):
    return JSONResponse(content={'message': 'OK'})


def test_is_allowed_within_limit():
    # Arrange
    identifier = 'user-a'
    limiter = RateLimiter(max_requests=3, window_seconds=10)
    limiter.reset(identifier)

    # Act
    results = [limiter.is_allowed(identifier) for _ in range(3)]

    # Assert
    for allowed, info in results:
        assert allowed is True
        assert 0 <= info['requests_remaining'] <= 2


def test_is_allowed_blocks_when_limit_exceeded():
    # Arrange
    identifier = 'user-b'
    limiter = RateLimiter(max_requests=2, window_seconds=10)
    limiter.reset(identifier)

    # Act
    limiter.is_allowed(identifier)
    limiter.is_allowed(identifier)
    allowed, info = limiter.is_allowed(identifier)

    # Assert
    assert allowed is False
    assert info['requests_remaining'] == 0
    assert 'reset_time' in info


def test_is_allowed_resets_after_window():
    # Arrange
    identifier = 'user-c'
    limiter = RateLimiter(max_requests=2, window_seconds=1)
    limiter.reset(identifier)

    limiter.is_allowed(identifier)
    limiter.is_allowed(identifier)

    time.sleep(1.1)

    # Act
    allowed, info = limiter.is_allowed(identifier)

    # Assert
    assert allowed is True
    assert info['requests_remaining'] == 1


def test_get_stats():
    # Arrange
    identifier = 'user-d'
    limiter = RateLimiter(max_requests=5, window_seconds=10)
    limiter.reset(identifier)
    limiter.is_allowed(identifier)
    limiter.is_allowed(identifier)

    # Act
    stats = limiter.get_stats(identifier)

    # Assert
    assert stats['current_requests'] == 2
    assert stats['requests_remaining'] == 3
    assert stats['limit'] == 5


def test_reset_clears_request_history():
    # Arrange
    identifier = 'user-e'
    limiter = RateLimiter(max_requests=2, window_seconds=10)
    limiter.is_allowed(identifier)
    limiter.is_allowed(identifier)

    # Act
    limiter.reset(identifier)
    stats = limiter.get_stats(identifier)

    # Assert
    assert stats['current_requests'] == 0
    assert stats['requests_remaining'] == 2


def test_rate_limit_decorator_allows_within_limit(client):
    # Arrange
    test_limiter.reset('testclient')

    # Act & Assert
    for _ in range(3):
        response = client.get('/limited')
        assert response.status_code == 200
        assert response.json()['message'] == 'OK'


def test_rate_limit_decorator_blocks_after_limit(client):
    # Arrange
    test_limiter.reset('testclient')

    # Act
    for _ in range(3):
        client.get('/limited')
    response = client.get('/limited')

    # Assert
    assert response.status_code == 429
    assert 'Rate limit exceeded' in response.text
