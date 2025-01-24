import os
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
    input_tokens_per_minute: Optional[int] = None
    output_tokens_per_minute: Optional[int] = None

class RateLimiter:
    def __init__(self):
        self.locks: Dict[str, Lock] = defaultdict(Lock)
        self.request_times: Dict[str, list] = defaultdict(list)
        self.token_counts: Dict[str, list] = defaultdict(list)  # List of (timestamp, token_count) tuples
        self.rate_limits: Dict[str, RateLimit] = {
            # OpenAI rate limits
            # https://platform.openai.com/docs/guides/rate-limits
            "openai": RateLimit(
                requests_per_minute=int(os.getenv("OPENAI_REQUESTS_PER_MINUTE", "500")),
                requests_per_hour=int(os.getenv("OPENAI_REQUESTS_PER_HOUR", "10000")),
                requests_per_day=int(os.getenv("OPENAI_REQUESTS_PER_DAY", "150000"))
            ),
            # Anthropic rate limits 
            # https://docs.anthropic.com/en/api/rate-limits
            "anthropic": RateLimit(
                requests_per_minute=int(os.getenv("ANTHROPIC_REQUESTS_PER_MINUTE", "50")),
                requests_per_hour=None,
                requests_per_day=None,
                input_tokens_per_minute=int(os.getenv("ANTHROPIC_INPUT_TOKENS_PER_MINUTE", "40000")),
                output_tokens_per_minute=int(os.getenv("ANTHROPIC_OUTPUT_TOKENS_PER_MINUTE", "8000"))
            ),
            # Azure OpenAI rate limits
            # https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits
            "azure": RateLimit(
                requests_per_minute=int(os.getenv("AZURE_REQUESTS_PER_MINUTE", "240")),
                requests_per_hour=int(os.getenv("AZURE_REQUESTS_PER_HOUR", "14400")),
                input_tokens_per_minute=int(os.getenv("AZURE_INPUT_TOKENS_PER_MINUTE", "60000")),
                output_tokens_per_minute=int(os.getenv("AZURE_OUTPUT_TOKENS_PER_MINUTE", "24000"))
            ),
            # Cohere rate limits
            # https://docs.cohere.com/reference/rate-limits
            "cohere": RateLimit(
                requests_per_minute=int(os.getenv("COHERE_REQUESTS_PER_MINUTE", "100")),
                requests_per_hour=int(os.getenv("COHERE_REQUESTS_PER_HOUR", "6000")),
                input_tokens_per_minute=int(os.getenv("COHERE_INPUT_TOKENS_PER_MINUTE", "30000"))
            ),
            # Add other provider limits as needed
        }

    def _cleanup_old_requests(self, provider: str, current_time: float):
        """Remove request timestamps and token counts older than 24 hours"""
        day_ago = current_time - 24 * 3600
        self.request_times[provider] = [
            t for t in self.request_times[provider] if t > day_ago
        ]
        self.token_counts[provider] = [
            (t, count) for t, count in self.token_counts[provider] if t > day_ago
        ]

    def _check_and_wait(self, provider: str, current_time: float, token_count: int = 0) -> float:
        """Check rate limits and return required wait time"""
        if provider not in self.rate_limits:
            return 0

        limits = self.rate_limits[provider]
        times = self.request_times[provider]
        tokens = self.token_counts[provider]
        
        # Check minute limit for requests
        minute_ago = current_time - 60
        minute_requests = sum(1 for t in times if t > minute_ago)
        if minute_requests >= limits.requests_per_minute:
            return 60 - (current_time - times[-limits.requests_per_minute])

        # Check minute limit for tokens
        if limits.input_tokens_per_minute or limits.output_tokens_per_minute:
            minute_tokens = sum(count for t, count in tokens if t > minute_ago)
            max_tokens_per_minute = (limits.input_tokens_per_minute or 0) + (limits.output_tokens_per_minute or 0)
            if max_tokens_per_minute and minute_tokens + token_count > max_tokens_per_minute:
                # Find the oldest token count that puts us over the limit
                sorted_tokens = sorted((t for t, _ in tokens if t > minute_ago))
                if sorted_tokens:
                    return 60 - (current_time - sorted_tokens[0])
                return 60

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

    def wait_if_needed(self, provider: str, token_count: int = 0):
        """Wait if necessary to comply with rate limits"""
        with self.locks[provider]:
            current_time = time.time()
            self._cleanup_old_requests(provider, current_time)
            
            wait_time = self._check_and_wait(provider, current_time, token_count)
            if wait_time > 0:
                time.sleep(wait_time)
            
            self.request_times[provider].append(time.time())
            if token_count:
                self.token_counts[provider].append((time.time(), token_count))

# Global rate limiter instance
rate_limiter = RateLimiter()
