from flask import Flask, request, jsonify
import base64
import os
import tempfile
import librosa
import numpy as np
from scipy import signal
from scipy.stats import kurtosis, skew
import io

app = Flask(__name__)

# API Key for authentication
API_KEY = "your_secure_api_key_here_123456"

def verify_api_key():
    """Verify API key from request headers"""
    auth_header = request.headers.get('Authorization') or request.headers.get('X-API-Key')
    if not auth_header:
        return False
    
    # Support both "Bearer <key>" and direct key
    if auth_header.startswith('Bearer '):
        provided_key = auth_header.replace('Bearer ', '')
    else:
        provided_key = auth_header
    
    return provided_key == API_KEY

def extract_audio_features(audio_path):
    """Extract comprehensive audio features for AI detection"""
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        features = {}
        
        # 1. Spectral Features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
        
        # 2. MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        for i in range(min(13, mfccs.shape[0])):
            features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
            features[f'mfcc_{i}_std'] = np.std(mfccs[i])
        
        # 3. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features['zcr_mean'] = np.mean(zcr)
        features['zcr_std'] = np.std(zcr)
        
        # 4. Energy and RMS
        rms = librosa.feature.rms(y=y)[0]
        features['rms_mean'] = np.mean(rms)
        features['rms_std'] = np.std(rms)
        
        # 5. Pitch and Harmonics
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if pitch_values:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_range'] = 0
        
        # 6. Temporal Features
        features['duration'] = len(y) / sr
        
        # 7. Spectral Flatness (AI voices tend to be flatter)
        spectral_flatness = librosa.feature.spectral_flatness(y=y)[0]
        features['spectral_flatness_mean'] = np.mean(spectral_flatness)
        features['spectral_flatness_std'] = np.std(spectral_flatness)
        
        # 8. Chroma features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features['chroma_mean'] = np.mean(chroma)
        features['chroma_std'] = np.std(chroma)
        
        # 9. Statistical measures
        features['audio_kurtosis'] = kurtosis(y)
        features['audio_skew'] = skew(y)
        
        return features
    
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return None

def detect_ai_voice(features):
    """
    Rule-based AI voice detection using audio features
    AI-generated voices typically have:
    - More uniform spectral characteristics
    - Less natural pitch variation
    - Smoother transitions
    - More consistent energy levels
    """
    
    if not features:
        return "HUMAN", 0.5, "Unable to extract features, defaulting to human"
    
    ai_indicators = 0
    total_checks = 0
    reasons = []
    
    # Check 1: Spectral Flatness (AI voices are often flatter)
    total_checks += 1
    if features.get('spectral_flatness_mean', 0) > 0.3:
        ai_indicators += 1
        reasons.append("High spectral flatness suggests synthetic generation")
    
    # Check 2: Pitch Variation (AI voices have less natural variation)
    total_checks += 1
    if features.get('pitch_std', 0) < 20:
        ai_indicators += 1
        reasons.append("Low pitch variation indicates artificial voice")
    
    # Check 3: Spectral Centroid Consistency (AI is more consistent)
    total_checks += 1
    if features.get('spectral_centroid_std', 0) < 300:
        ai_indicators += 1
        reasons.append("Very consistent spectral centroid pattern")
    
    # Check 4: Energy Consistency (AI has more uniform energy)
    total_checks += 1
    if features.get('rms_std', 0) < 0.02:
        ai_indicators += 1
        reasons.append("Unnaturally consistent energy levels")
    
    # Check 5: Zero Crossing Rate variation
    total_checks += 1
    if features.get('zcr_std', 0) < 0.02:
        ai_indicators += 1
        reasons.append("Limited zero-crossing rate variation")
    
    # Check 6: MFCC patterns (AI voices have different MFCC patterns)
    total_checks += 1
    mfcc_stds = [features.get(f'mfcc_{i}_std', 0) for i in range(5)]
    if mfcc_stds and np.mean(mfcc_stds) < 10:
        ai_indicators += 1
        reasons.append("MFCC patterns suggest synthetic voice")
    
    # Check 7: Spectral Bandwidth (AI voices often have narrower bandwidth)
    total_checks += 1
    if features.get('spectral_bandwidth_mean', 0) < 1000:
        ai_indicators += 1
        reasons.append("Narrow spectral bandwidth typical of AI")
    
    # Check 8: Chroma variation
    total_checks += 1
    if features.get('chroma_std', 0) < 0.1:
        ai_indicators += 1
        reasons.append("Limited chroma variation")
    
    # Calculate confidence
    ai_score = ai_indicators / total_checks
    
    # Determine classification
    if ai_score > 0.55:  # More than 55% AI indicators
        classification = "AI_GENERATED"
        confidence = min(0.6 + (ai_score - 0.55) * 0.8, 0.95)
        explanation = "AI-generated voice detected. " + "; ".join(reasons[:3])
    else:
        classification = "HUMAN"
        confidence = min(0.6 + (1 - ai_score) * 0.8, 0.95)
        explanation = "Human voice detected with natural variations in pitch, energy, and spectral characteristics"
    
    return classification, round(confidence, 2), explanation

@app.route('/detect', methods=['POST'])
def detect_voice():
    """Main endpoint for voice detection"""
    
    # Verify API key
    if not verify_api_key():
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid or missing API key"
        }), 401
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'audio' not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing 'audio' field in request body"
            }), 400
        
        audio_base64 = data['audio']
        
        # Decode base64 audio
        try:
            audio_bytes = base64.b64decode(audio_base64)
        except Exception as e:
            return jsonify({
                "error": "Bad Request",
                "message": f"Invalid base64 encoding: {str(e)}"
            }), 400
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            # Extract features
            features = extract_audio_features(tmp_path)
            
            # Detect AI voice
            classification, confidence, explanation = detect_ai_voice(features)
            
            # Prepare response
            response = {
                "classification": classification,
                "confidence": confidence,
                "explanation": explanation,
                "language_support": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
                "status": "success"
            }
            
            return jsonify(response), 200
        
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": f"Error processing request: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Voice Detection API is running",
        "version": "1.0.0"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """API information endpoint"""
    return jsonify({
        "name": "AI-Generated Voice Detection API",
        "version": "1.0.0",
        "description": "Detects whether a voice sample is AI-generated or human",
        "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
        "endpoints": {
            "/detect": "POST - Main detection endpoint (requires API key)",
            "/health": "GET - Health check",
            "/": "GET - API information"
        },
        "authentication": "API key required in 'Authorization' or 'X-API-Key' header"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
