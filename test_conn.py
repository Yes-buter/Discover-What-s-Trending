import asyncio
from supabase import create_client, Client
from api.core.config import settings
import httpx
import os

async def test_connection():
    print(f"Testing connection to: {settings.SUPABASE_URL}")
    
    print("\n--- Attempt 7: Explicit Proxy 7890 + Verify=True ---")
    proxies = "http://127.0.0.1:7890"
    try:
        async with httpx.AsyncClient(proxy=proxies, verify=True) as client:
            response = await client.get(f"{settings.SUPABASE_URL}/auth/v1/health")
            print(f"Health check status: {response.status_code}")
    except Exception as e:
        print(f"Failed: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection())
