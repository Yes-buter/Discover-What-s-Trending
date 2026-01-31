from supabase import create_client, Client
from .config import settings
import os

# Fix for SSL/Connection errors in some network environments (e.g. China)
# Try to detect and use common local proxy ports if no proxy is set
if not os.environ.get("HTTP_PROXY") and not os.environ.get("HTTPS_PROXY"):
    # Common proxy ports: 7890 (Clash), 10809 (v2ray)
    # We found 7890 works in this environment
    proxy_url = "http://127.0.0.1:7890"
    print(f"Applying automatic proxy fix: {proxy_url}")
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
