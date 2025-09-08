import os

JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY", default="f040763a24b74e99bae5f30d15215c68")
"""API key used in Jellyfin"""

JELLYFIN_URL = os.getenv("JELLYFIN_URL", default="http://localhost:8096")
"""URL to connect to Jellyfin"""
