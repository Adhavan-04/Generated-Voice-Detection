# AI-Generated Voice Detection API

🎤 Multi-language voice detection system for identifying AI-generated vs human voices

## 🌟 Features

- Detects AI-generated voices vs human voices
- Supports 5 languages: Tamil, English, Hindi, Malayalam, Telugu
- REST API with JSON responses
- Base64 audio input support
- Confidence scoring (0.0 - 1.0)
- Secure API key authentication

## 🚀 Quick Start

### Local Development

1. **Clone/Download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the API**
```bash
python app.py
```

API will be available at: `http://localhost:5000`

### Test the API

```bash
python test_api.py
```

## 📡 API Endpoints

### 1. Detection Endpoint

**POST** `/detect`

Analyzes audio and returns classification.

**Headers:**
```
Content-Type: application/json
Authorization: Bearer your_secure_api_key_here_123456
```

**Request Body:**
```json
{
  "audio": "BASE64_ENCODED_MP3_AUDIO"
}
```

**Response (Success):**
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.87,
  "explanation": "AI-generated voice detected. High spectral flatness suggests synthetic generation",
  "language_support": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
  "status": "success"
}
```

**Response (Error):**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### 2. Health Check

**GET** `/health`

Check API status.

**Response:**
```json
{
  "status": "healthy",
  "message": "AI Voice Detection API is running",
  "version": "1.0.0"
}
```

### 3. API Info

**GET** `/`

Get API information and available endpoints.

## 🔐 Authentication

All detection requests require an API key in the Authorization header:

```
Authorization: Bearer your_secure_api_key_here_123456
```

Or alternatively:

```
X-API-Key: your_secure_api_key_here_123456
```

## 🧪 How It Works

The API uses advanced audio signal processing to detect AI-generated voices:

### Audio Features Analyzed:

1. **Spectral Features**
   - Spectral centroid (frequency center of mass)
   - Spectral rolloff (frequency below which 85% of energy is contained)
   - Spectral bandwidth
   - Spectral flatness

2. **MFCC (Mel-Frequency Cepstral Coefficients)**
   - 20 MFCC coefficients analyzed
   - Captures timbral characteristics

3. **Temporal Features**
   - Zero crossing rate
   - RMS energy
   - Duration

4. **Pitch Analysis**
   - Mean pitch
   - Pitch variation (standard deviation)
   - Pitch range

5. **Harmonic Features**
   - Chroma features
   - Harmonic-to-noise ratio patterns

### Detection Logic:

AI-generated voices typically exhibit:
- ✓ More uniform spectral characteristics
- ✓ Less natural pitch variation
- ✓ Smoother energy transitions
- ✓ More consistent MFCC patterns
- ✓ Higher spectral flatness
- ✓ Narrower spectral bandwidth

The system checks multiple indicators and calculates a confidence score.

## 📊 Classification Output

- **AI_GENERATED**: Voice is likely synthesized by AI
- **HUMAN**: Voice is likely from a real human
- **Confidence**: 0.0 to 1.0 (higher = more confident)

## 🌐 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions on:

- ✅ Render.com (Recommended - Free)
- ✅ Railway.app (Free)
- ✅ PythonAnywhere (Free)
- ✅ Vercel (Free)

## 📝 Example Usage

### Python

```python
import requests
import base64

# Read audio file
with open('voice_sample.mp3', 'rb') as f:
    audio_data = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    'https://your-api.com/detect',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your_api_key'
    },
    json={'audio': audio_data}
)

result = response.json()
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']}")
```

### cURL

```bash
curl -X POST https://your-api.com/detect \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "audio": "BASE64_AUDIO_HERE"
  }'
```

### JavaScript

```javascript
const audioFile = document.getElementById('audioInput').files[0];
const reader = new FileReader();

reader.onload = async function(e) {
  const base64Audio = btoa(
    new Uint8Array(e.target.result)
      .reduce((data, byte) => data + String.fromCharCode(byte), '')
  );
  
  const response = await fetch('https://your-api.com/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_api_key'
    },
    body: JSON.stringify({ audio: base64Audio })
  });
  
  const result = await response.json();
  console.log(result);
};

reader.readAsArrayBuffer(audioFile);
```

## 🎯 Hackathon Submission Checklist

- [ ] Deploy API to free hosting platform
- [ ] Test with sample audio files
- [ ] Verify authentication works
- [ ] Check response format matches requirements
- [ ] Submit API endpoint URL
- [ ] Submit API key
- [ ] Ensure API is publicly accessible
- [ ] Test API stability (multiple requests)

## 🔧 Configuration

### Change API Key

In `app.py`, modify:
```python
API_KEY = "your_secure_api_key_here_123456"
```

### Adjust Detection Threshold

In `detect_ai_voice()` function, modify:
```python
if ai_score > 0.55:  # Change this threshold (0.0 to 1.0)
```

### Customize Port

```python
app.run(host='0.0.0.0', port=5000)  # Change port number
```

## 📦 Dependencies

- Flask: Web framework
- librosa: Audio analysis
- numpy: Numerical computations
- scipy: Signal processing
- soundfile: Audio file I/O
- gunicorn: Production server

## 🐛 Troubleshooting

### Import Error: librosa

```bash
# Install system dependencies (Linux)
sudo apt-get install libsndfile1

# Install Python package
pip install librosa soundfile
```

### API returns 500 Error

- Check server logs for detailed error
- Verify audio is valid MP3 format
- Ensure all dependencies are installed

### Low Accuracy

The current implementation uses rule-based detection. For better accuracy:
1. Collect labeled training data
2. Train a machine learning model
3. Use deep learning (CNN/RNN) for audio classification

## 🎓 Learning Resources

- Audio Signal Processing: [librosa documentation](https://librosa.org/)
- Flask API Development: [Flask docs](https://flask.palletsprojects.com/)
- Audio ML: [Audio Classification Tutorial](https://www.tensorflow.org/tutorials/audio/simple_audio)

## 📄 License

This project is created for hackathon purposes. Feel free to use and modify.

## 🤝 Support

For issues or questions:
1. Check the DEPLOYMENT_GUIDE.md
2. Review error messages carefully
3. Test locally before deploying
4. Verify API key authentication

---

**Built for AI Voice Detection Hackathon** 🏆

Good luck! 🚀
