import time
from datetime import datetime
from typing import Optional

from requests import Response

RATE_LIMIT_RESPONSE_TEXT = "You exceeded the rate limit"


class RateLimit:
    """
    Class that represents a rate-limit.
    """

    def __init__(self, reset_time: datetime):
        self.reset_time = reset_time

    @classmethod
    def from_response(cls, response: Response):
        if response.ok or response.text != RATE_LIMIT_RESPONSE_TEXT:
            return None

        reset_timestamp: str = response.headers.get("X-Ratelimit-Reset", "")
        if reset_timestamp.isdigit():
            return cls(reset_time=datetime.fromtimestamp(int(reset_timestamp)))

        return None

    def reset_timedelta(self, utcnow: Optional[datetime] = None):
        """
        Return a timedelta object representing the delta between the current UTC time and the reset time.
        Note the delta may be negative.

        :param utcnow: if passed, this is used instead of datetime.utcnow()
        """
        if utcnow is None:
            utcnow = datetime.utcnow()

        return self.reset_time - utcnow

    def wait_until_expiration(self, *, wait_function=time.sleep):
        """
        Wait until the rate limit expires.
        """
        delta = self.reset_timedelta()
        wait_seconds = delta.total_seconds()
        if wait_seconds >= 0:
            wait_function(wait_seconds)
