import os

from redis import Redis

SESSION_REDIS_HOST = os.getenv("SESSION_REDIS_HOST", "localhost")
SESSION_REDIS_PORT = os.getenv("SESSION_REDIS_PORT", 6379)
SESSION_REDIS_DB = os.getenv("SESSION_REDIS_DB", 0)
SESSION_REDIS_PASSWORD = os.getenv("SESSION_REDIS_PASSWORD")


class Session(object):
    """
    Simple Redis based session storage class.
    """

    def __init__(self):
        self._r = Redis(
            host=SESSION_REDIS_HOST, port=SESSION_REDIS_PORT, db=SESSION_REDIS_DB, password=SESSION_REDIS_PASSWORD
        )

    def exists(self, sender_id, mode_key):
        return self._r.hexists(sender_id, mode_key)

    def reset(self, sender_id, *enabled_modes):
        """
        Removes all modes from the session and sets the given modes names as enabled
        """
        p = self._r.pipeline()
        p.delete(sender_id)
        if enabled_modes:
            p.hmset(sender_id, {mode: 1 for mode in enabled_modes})
        p.execute()

    def search_by_id(self, sender_id):
        """
        Checks if the search_by_id mode is enabled for the given sender id
        """
        return self.exists(sender_id, "search_by_id")

    def search_by_name(self, sender_id):
        """
        Checks if the search_by_name mode is enabled for the given sender id
        """
        return self.exists(sender_id, "search_by_name")
