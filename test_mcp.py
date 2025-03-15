import requests
import json

def test_health():
    try:
        response = requests.get("http://localhost:8080/health")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_supabase_list_tables():
    try:
        payload = {
            "action": "list_tables",
            "parameters": {}
        }
        response = requests.post(
            "http://localhost:8080/supabase", 
            json=payload
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_youtube_transcript():
    try:
        payload = {
            "action": "get_transcript",
            "parameters": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "lang": "en"
            }
        }
        response = requests.post(
            "http://localhost:8080/youtube", 
            json=payload
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing MCP Server...")
    
    print("\n1. Testing Health Endpoint")
    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        
    print("\n2. Testing Supabase List Tables")
    if test_supabase_list_tables():
        print("✅ Supabase list tables test passed")
    else:
        print("❌ Supabase list tables test failed")
        
    print("\n3. Testing YouTube Transcript")
    if test_youtube_transcript():
        print("✅ YouTube transcript test passed")
    else:
        print("❌ YouTube transcript test failed") 