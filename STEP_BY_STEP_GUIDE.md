# Step-by-Step Implementation Guide

## Complete Setup - From Zero to Deployed API

### Phase 1: Local Setup (30 minutes)

#### Step 1: Install Python
1. Download Python 3.9+ from python.org
2. Install with "Add to PATH" checked
3. Verify: Open terminal/cmd and type:
   ```bash
   python --version
   ```

#### Step 2: Create Project Folder
```bash
mkdir ai-voice-detection
cd ai-voice-detection
```

#### Step 3: Download Project Files
Save these files in your project folder:
- app.py (main API code)
- requirements.txt (dependencies)
- test_api.py (testing script)
- Procfile (deployment config)
- README.md (documentation)
- DEPLOYMENT_GUIDE.md (deployment steps)

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**If errors occur:**
- Windows: You may need Microsoft C++ Build Tools
- Linux: `sudo apt-get install libsndfile1 ffmpeg`
- Mac: `brew install libsndfile`

#### Step 5: Test Locally
```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

Open browser: http://localhost:5000
You should see API info.

---

### Phase 2: GitHub Setup (15 minutes)

#### Step 1: Create GitHub Account
Go to github.com and sign up (free)

#### Step 2: Create New Repository
1. Click "New repository"
2. Name: `ai-voice-detection`
3. Choose "Public"
4. Click "Create repository"

#### Step 3: Upload Files
Two options:

**Option A: Using GitHub Web Interface (Easier)**
1. Click "uploading an existing file"
2. Drag and drop all your files
3. Click "Commit changes"

**Option B: Using Git Command Line**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-detection.git
git push -u origin main
```

---

### Phase 3: Deploy on Render.com (20 minutes)

#### Step 1: Sign Up
1. Go to render.com
2. Click "Get Started for Free"
3. Sign up with GitHub

#### Step 2: Connect Repository
1. Click "New +" → "Web Service"
2. Click "Connect account" for GitHub
3. Find and select your `ai-voice-detection` repository

#### Step 3: Configure Service
Fill in these details:
- **Name**: `ai-voice-detection` (or any name you want)
- **Region**: Select closest to you
- **Branch**: `main`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: Free

#### Step 4: Add Environment Variables (Optional)
Click "Advanced" → "Add Environment Variable"
- Key: `API_KEY`
- Value: `VoiceDetect_2024_SecureKey_xyz789`

(If you skip this, the key from app.py will be used)

#### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your API URL will be shown (e.g., `https://ai-voice-detection.onrender.com`)

#### Step 6: Test Deployed API
```bash
curl https://YOUR-APP.onrender.com/health
```

You should see:
```json
{
  "status": "healthy",
  "message": "AI Voice Detection API is running"
}
```

---

### Phase 4: Test with Audio (15 minutes)

#### Step 1: Prepare Test Audio
You need an MP3 audio file. Options:
1. Download sample from hackathon organizers
2. Record your own voice (use phone/computer)
3. Use online TTS to generate AI voice

#### Step 2: Convert to Base64

**Using Python:**
```python
import base64

with open('your_audio.mp3', 'rb') as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    print(audio_base64)
```

**Using Online Tool:**
- Go to base64encode.org
- Upload your MP3
- Copy the base64 string

#### Step 3: Test API

**Using test_api.py:**
1. Open `test_api.py`
2. Update these lines:
   ```python
   API_URL = "https://YOUR-APP.onrender.com/detect"
   API_KEY = "VoiceDetect_2024_SecureKey_xyz789"
   ```
3. Uncomment and update:
   ```python
   test_api_with_audio_file("your_audio.mp3")
   ```
4. Run:
   ```bash
   python test_api.py
   ```

**Using cURL:**
```bash
curl -X POST https://YOUR-APP.onrender.com/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VoiceDetect_2024_SecureKey_xyz789" \
  -d '{
    "audio": "YOUR_BASE64_AUDIO_STRING_HERE"
  }'
```

**Using Postman:**
1. Download Postman (free)
2. Create new POST request
3. URL: `https://YOUR-APP.onrender.com/detect`
4. Headers:
   - `Content-Type`: `application/json`
   - `Authorization`: `Bearer VoiceDetect_2024_SecureKey_xyz789`
5. Body (raw JSON):
   ```json
   {
     "audio": "YOUR_BASE64_STRING"
   }
   ```
6. Click Send

---

### Phase 5: Hackathon Submission (5 minutes)

Submit these details to the hackathon platform:

1. **API Endpoint URL**: 
   ```
   https://YOUR-APP.onrender.com/detect
   ```

2. **API Key**: 
   ```
   VoiceDetect_2024_SecureKey_xyz789
   ```

3. **Additional Notes** (optional):
   ```
   - API supports Base64-encoded MP3 audio
   - Returns classification (AI_GENERATED or HUMAN)
   - Includes confidence score (0.0-1.0)
   - Supports Tamil, English, Hindi, Malayalam, Telugu
   - Response format: JSON
   ```

---

### Common Issues & Solutions

#### Issue 1: "Module not found" error
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Issue 2: Render deployment fails
**Solution:**
- Check your Procfile exists
- Verify requirements.txt has all packages
- Check deployment logs in Render dashboard
- Ensure Python version is 3.9+

#### Issue 3: API returns 401 Unauthorized
**Solution:**
- Verify API key matches in your test script
- Check Authorization header format
- Try both formats: `Bearer KEY` and just `KEY`

#### Issue 4: API returns 400 Bad Request
**Solution:**
- Verify audio is properly base64 encoded
- Check JSON format (use JSON validator)
- Ensure 'audio' field is present

#### Issue 5: Render API is slow (first request)
**Solution:**
- This is normal for free tier
- Free services "sleep" after 15 min inactivity
- First request takes ~1 minute to wake up
- Subsequent requests are fast

---

### Testing Checklist

Before submitting, verify:

- [ ] API is accessible publicly (test from different device)
- [ ] Health endpoint works: `/health`
- [ ] Authentication works with API key
- [ ] Detection endpoint accepts base64 audio
- [ ] Response format matches requirements:
  - [ ] Has "classification" field
  - [ ] Has "confidence" field (0.0-1.0)
  - [ ] Has "explanation" field
  - [ ] Has "status" field
- [ ] Works with multiple audio samples
- [ ] Handles errors gracefully (test with invalid input)

---

### Alternative Deployment Options

If Render doesn't work, try these:

**Railway.app:**
1. Go to railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Add API_KEY environment variable
5. Done! Get your URL from dashboard

**Vercel:**
1. Install: `npm install -g vercel`
2. Add vercel.json to your project:
   ```json
   {
     "builds": [{"src": "app.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "app.py"}]
   }
   ```
3. Run: `vercel --prod`
4. Get your URL

---

### Getting Sample Audio for Testing

**Option 1: Record yourself**
- Use phone voice recorder
- Say a few sentences in any supported language
- Export as MP3

**Option 2: Generate AI voice (for testing AI detection)**
- Use ElevenLabs.io (free tier available)
- Use Google TTS, Amazon Polly, or Microsoft TTS
- Generate speech and download MP3

**Option 3: Download from hackathon**
- Use the sample audio provided in hackathon Google Drive
- Download and use for testing

---

### Tips for Success

1. **Test thoroughly before submitting**
   - Test with multiple audio samples
   - Test different languages
   - Test both AI and human voices

2. **Monitor your deployment**
   - Check Render logs for errors
   - Test API every few hours during hackathon

3. **Keep it simple**
   - Current solution works for hackathon
   - Don't over-engineer for now
   - Focus on making it reliable

4. **Have a backup**
   - Deploy on both Render and Railway
   - Submit the more stable one

5. **Document everything**
   - Note your API URL
   - Save your API key
   - Keep test results

---

### Next Steps (After Hackathon)

If you want to improve the solution:

1. **Collect training data**
   - Gather human voice samples
   - Gather AI-generated samples
   - Label them correctly

2. **Train ML model**
   ```python
   from sklearn.ensemble import RandomForestClassifier
   # Extract features from training data
   # Train classifier
   # Replace rule-based detection
   ```

3. **Use deep learning**
   - PyTorch or TensorFlow
   - CNN for audio classification
   - Fine-tune on your data

4. **Add more features**
   - Language detection
   - Speaker identification
   - Emotion analysis

---

### Support & Resources

- **Render Documentation**: docs.render.com
- **Flask Tutorial**: flask.palletsprojects.com
- **Librosa Tutorial**: librosa.org/doc/latest/tutorial.html
- **Audio ML Course**: coursera.org/learn/audio-signal-processing

---

**You're ready to go! Follow these steps and you'll have a working API in ~1 hour.**

Good luck with your hackathon! 🎉🚀
