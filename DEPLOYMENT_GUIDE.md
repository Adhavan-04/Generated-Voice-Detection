# Deployment Guide - AI Voice Detection API

## Option 1: Deploy on Render.com (FREE - RECOMMENDED)

Render.com offers free hosting for web services. Follow these steps:

### Step 1: Prepare Your Code

1. Create a GitHub account if you don't have one: https://github.com
2. Create a new repository (e.g., "ai-voice-detection")
3. Upload these files to your repository:
   - app.py
   - requirements.txt
   - Procfile (create this - see below)

### Step 2: Create Procfile

Create a file named `Procfile` (no extension) with this content:
```
web: gunicorn app:app
```

### Step 3: Deploy on Render

1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ai-voice-detection-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
5. Add Environment Variable:
   - Key: `API_KEY`
   - Value: your_secure_api_key_here_123456
6. Click "Create Web Service"

Your API will be deployed at: `https://ai-voice-detection-api.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~1 minute.

---

## Option 2: Deploy on Railway.app (FREE)

Railway offers 500 hours/month free:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Add environment variable `API_KEY` in settings
7. Your API URL will be provided

---

## Option 3: Deploy on PythonAnywhere (FREE)

PythonAnywhere offers limited free tier:

1. Sign up at https://www.pythonanywhere.com
2. Go to "Web" tab
3. Click "Add a new web app"
4. Select "Flask"
5. Upload your files
6. Configure WSGI file to point to your app
7. Install requirements in console: `pip install -r requirements.txt`

---

## Option 4: Deploy on Vercel (FREE - Serverless)

Vercel offers serverless deployment:

1. Install Vercel CLI: `npm install -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Run: `vercel --prod`

---

## Testing Your Deployed API

### Update API_KEY in app.py

Before deploying, change this line in app.py:
```python
API_KEY = "your_secure_api_key_here_123456"
```
To a strong, unique key like:
```python
API_KEY = "VoiceDetect_2024_SecureKey_xyz789abc"
```

### Test with cURL

```bash
# Health check
curl https://your-api-url.com/health

# Test detection (replace with your audio base64)
curl -X POST https://your-api-url.com/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VoiceDetect_2024_SecureKey_xyz789abc" \
  -d '{
    "audio": "BASE64_ENCODED_AUDIO_HERE"
  }'
```

### Test with Python

Use the provided `test_api.py` script:
1. Update API_URL to your deployed URL
2. Update API_KEY to match your deployment
3. Run: `python test_api.py`

---

## Hackathon Submission

Submit:
1. **API Endpoint**: `https://your-api-url.com/detect`
2. **API Key**: `VoiceDetect_2024_SecureKey_xyz789abc` (or whatever you set)
3. **Documentation**: Include supported format (Base64 MP3) and expected response

---

## Expected API Response Format

```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "explanation": "AI-generated voice detected. High spectral flatness suggests synthetic generation; Low pitch variation indicates artificial voice",
  "language_support": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
  "status": "success"
}
```

---

## Troubleshooting

### API returns 401 Unauthorized
- Check your API key matches in both app and test script

### API returns 400 Bad Request
- Ensure audio is properly base64 encoded
- Check JSON payload format

### Deployment fails
- Verify requirements.txt has all dependencies
- Check Python version compatibility (use 3.9+)
- Review deployment logs in platform dashboard

### Audio processing errors
- Ensure librosa is installed
- Check audio file format (MP3)
- Verify base64 encoding is correct

---

## Improving Accuracy (Optional)

For better detection:
1. Collect training data (human vs AI voices)
2. Train a machine learning model (scikit-learn, PyTorch)
3. Replace rule-based detection with ML model
4. Fine-tune on multilingual data

Basic ML approach:
```python
from sklearn.ensemble import RandomForestClassifier
# Train on features extracted from known samples
# Use model.predict(features) instead of rule-based logic
```

---

## Free Resources

- **Render.com**: Best for simple deployment
- **Railway.app**: Good free tier, easy to use
- **PythonAnywhere**: Traditional hosting
- **Vercel**: Serverless, good for APIs
- **Hugging Face Spaces**: Can host Gradio/Streamlit apps

Good luck with your hackathon! 🚀
