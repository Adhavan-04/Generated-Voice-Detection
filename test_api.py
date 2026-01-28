import requests
import base64
import json

# Configuration
API_URL = "http://localhost:5000/detect"  # Change this to your deployed URL
API_KEY = "your_secure_api_key_here_123456"

def test_api_with_audio_file(audio_file_path):
    """Test the API with a local audio file"""
    
    # Read and encode audio file
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Prepare request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    payload = {
        'audio': audio_base64
    }
    
    # Send request
    print(f"Testing API at: {API_URL}")
    print(f"Audio file: {audio_file_path}")
    print("Sending request...\n")
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()

def test_api_with_url(audio_url):
    """Test the API with an audio URL"""
    
    # Download audio
    print(f"Downloading audio from: {audio_url}")
    audio_response = requests.get(audio_url)
    
    if audio_response.status_code != 200:
        print(f"Failed to download audio: {audio_response.status_code}")
        return
    
    # Encode to base64
    audio_base64 = base64.b64encode(audio_response.content).decode('utf-8')
    
    # Prepare request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    payload = {
        'audio': audio_base64
    }
    
    # Send request
    print(f"Testing API at: {API_URL}")
    print("Sending request...\n")
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()

def test_health_check():
    """Test the health endpoint"""
    response = requests.get(API_URL.replace('/detect', '/health'))
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("=" * 60)
    print("AI Voice Detection API - Test Script")
    print("=" * 60)
    print()
    
    # Test health check
    test_health_check()
    print()
    
    # Test with a sample audio file (you need to provide this)
    # Uncomment one of the following based on what you have:
    
    # Option 1: Test with local file
    # test_api_with_audio_file("sample_audio.mp3")
    
    # Option 2: Test with URL
    # test_api_with_url("https://example.com/sample_audio.mp3")
    
    print("\nTo test with your own audio:")
    print("1. Uncomment the appropriate test function above")
    print("2. Provide your audio file path or URL")
    print("3. Run this script again")
