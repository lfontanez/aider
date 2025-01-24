import time
from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from typing import Dict, Optional

@dataclass
class RateLimit:
    requests_per_minute: int
    requests_per_hour: Optional[int] = None
    requests_per_day: Optional[int] = None

class RateLimiter:
    def __init__(self):
        self.locks: Dict[str, Lock] = defaultdict(Lock)
        self.request_times: Dict[str, list] = defaultdict(list)
        self.rate_limits: Dict[str, RateLimit] = {
            "openai": RateLimit(
                requests_per_minute=500,
                requests_per_hour=10000,
                requests_per_day=150000
            ),
            "anthropic": RateLimit(
                requests_per_minute=50,
                requests_per_hour=1000
            ),
            # Add other provider limits as needed
        }

    def _cleanup_old_requests(self, provider: str, current_time: float):
        """Remove request timestamps older than 24 hours"""
        day_ago = current_time - 24 * 3600
        self.request_times[provider] = [
            t for t in self.request_times[provider] if t > day_ago
        ]

    def _check_and_wait(self, provider: str, current_time: float) -> float:
        """Check rate limits and return required wait time"""
        if provider not in self.rate_limits:
            return 0

        limits = self.rate_limits[provider]
        times = self.request_times[provider]
        
        # Check minute limit
        minute_ago = current_time - 60
        minute_requests = sum(1 for t in times if t > minute_ago)
        if minute_requests >= limits.requests_per_minute:
            return 60 - (current_time - times[-limits.requests_per_minute])

        # Check hour limit
        if limits.requests_per_hour:
            hour_ago = current_time - 3600
            hour_requests = sum(1 for t in times if t > hour_ago)
            if hour_requests >= limits.requests_per_hour:
                return 3600 - (current_time - times[-limits.requests_per_hour])

        # Check day limit
        if limits.requests_per_day:
            day_ago = current_time - 24 * 3600
            day_requests = sum(1 for t in times if t > day_ago)
            if day_requests >= limits.requests_per_day:
                return 24 * 3600 - (current_time - times[-limits.requests_per_day])

        return 0

    def wait_if_needed(self, provider: str):
        """Wait if necessary to comply with rate limits"""
        with self.locks[provider]:
            current_time = time.time()
            self._cleanup_old_requests(provider, current_time)
            
            wait_time = self._check_and_wait(provider, current_time)
            if wait_time > 0:
                time.sleep(wait_time)
            
            self.request_times[provider].append(time.time())

# Global rate limiter instance
rate_limiter = RateLimiter()
