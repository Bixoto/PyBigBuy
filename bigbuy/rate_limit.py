import time
from datetime import datetime, timedelta
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
        if response.ok:
            return None

        if response.text != RATE_LIMIT_RESPONSE_TEXT:
            return None

        reset_timestamp: str = response.headers.get("X-Ratelimit-Reset", "")
        if reset_timestamp and reset_timestamp.isdigit():
            return cls(reset_time=datetime.fromtimestamp(int(reset_timestamp)))

    def reset_timedelta(self, utcnow: Optional[datetime] = None):
        """
        Return a timedelta object representing the delta between the current UTC time and the reset time.
        Return None if it would be negative (i.e. the rest time is in the past).

        :param utcnow: if passed, this is used instead of datetime.utcnow()
        """
        if not self.reset_time:
            return

        if utcnow is None:
            utcnow = datetime.utcnow()

        delta = self.reset_time - utcnow
        if delta <= timedelta(0):
            return

        return delta

    def wait_until_expiration(self, *, wait_function=time.sleep, additional_delay=0.01):
        """
        Wait until the rate limit expires and return True.
        If the rate limit is invalid, don’t do anything and return False.
        """
        if delta := self.reset_timedelta():
            wait_seconds = delta.total_seconds()
            wait_function(wait_seconds + additional_delay)
            return True
        return False
