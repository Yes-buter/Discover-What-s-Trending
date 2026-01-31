import httpx
import asyncio

async def register():
    url = "http://localhost:8000/api/auth/signup"
    data = {
        "email": "15802081029_new@qq.com",
        "password": "123456", 
        "username": "123"
    }
    print(f"Attempting to register with: {data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(register())
