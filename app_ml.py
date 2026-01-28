"""
Advanced ML-Based Voice Detection (Optional Upgrade)

This is an enhanced version using machine learning for better accuracy.
To use this:
1. Collect training data (AI and human voice samples)
2. Run train_model() to create model.pkl
3. Replace the detect_ai_voice() function in app.py with ml_detect_ai_voice()

Note: This requires training data which you'll need to collect.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

def extract_ml_features(audio_path):
    """Extract features optimized for ML model"""
    import librosa
    
    y, sr = librosa.load(audio_path, sr=None)
    
    features = []
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    features.extend([
        np.mean(spectral_centroids),
        np.std(spectral_centroids),
        np.max(spectral_centroids),
        np.min(spectral_centroids)
    ])
    
    # MFCCs (more coefficients for ML)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    for i in range(20):
        features.extend([
            np.mean(mfccs[i]),
            np.std(mfccs[i]),
            np.max(mfccs[i]),
            np.min(mfccs[i])
        ])
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    features.extend([np.mean(zcr), np.std(zcr)])
    
    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    features.extend([np.mean(rms), np.std(rms)])
    
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    features.extend([np.mean(rolloff), np.std(rolloff)])
    
    # Spectral bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    features.extend([np.mean(bandwidth), np.std(bandwidth)])
    
    # Spectral flatness
    flatness = librosa.feature.spectral_flatness(y=y)[0]
    features.extend([np.mean(flatness), np.std(flatness)])
    
    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features.extend([np.mean(chroma), np.std(chroma)])
    
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    features.append(tempo)
    
    return np.array(features)

def train_model(training_data_folder):
    """
    Train ML model on collected data
    
    Expected folder structure:
    training_data/
        human/
            sample1.mp3
            sample2.mp3
            ...
        ai/
            sample1.mp3
            sample2.mp3
            ...
    """
    
    print("Loading training data...")
    X = []
    y = []
    
    # Load human samples
    human_folder = os.path.join(training_data_folder, 'human')
    for filename in os.listdir(human_folder):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            try:
                filepath = os.path.join(human_folder, filename)
                features = extract_ml_features(filepath)
                X.append(features)
                y.append(0)  # 0 = Human
                print(f"Loaded human sample: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    # Load AI samples
    ai_folder = os.path.join(training_data_folder, 'ai')
    for filename in os.listdir(ai_folder):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            try:
                filepath = os.path.join(ai_folder, filename)
                features = extract_ml_features(filepath)
                X.append(features)
                y.append(1)  # 1 = AI
                print(f"Loaded AI sample: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"\nTraining on {len(X)} samples...")
    print(f"Human samples: {np.sum(y == 0)}")
    print(f"AI samples: {np.sum(y == 1)}")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_scaled, y)
    
    print("\nTraining complete!")
    
    # Save model and scaler
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("Model saved as model.pkl")
    print("Scaler saved as scaler.pkl")
    
    # Print feature importances
    importances = model.feature_importances_
    print("\nTop 10 most important features:")
    indices = np.argsort(importances)[::-1][:10]
    for i, idx in enumerate(indices):
        print(f"{i+1}. Feature {idx}: {importances[idx]:.4f}")
    
    return model, scaler

def ml_detect_ai_voice(audio_path):
    """
    ML-based detection (replaces rule-based detection)
    
    Use this function in app.py instead of detect_ai_voice()
    """
    
    # Load model and scaler
    if not os.path.exists('model.pkl') or not os.path.exists('scaler.pkl'):
        return "HUMAN", 0.5, "ML model not trained. Using default classification."
    
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    try:
        # Extract features
        features = extract_ml_features(audio_path)
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        if prediction == 1:  # AI
            classification = "AI_GENERATED"
            confidence = probabilities[1]
            explanation = f"ML model detected AI voice with {confidence*100:.1f}% confidence based on spectral and temporal patterns"
        else:  # Human
            classification = "HUMAN"
            confidence = probabilities[0]
            explanation = f"ML model detected human voice with {confidence*100:.1f}% confidence based on natural variation patterns"
        
        return classification, round(confidence, 2), explanation
    
    except Exception as e:
        return "HUMAN", 0.5, f"Error in ML detection: {str(e)}"

# Example usage for training
if __name__ == "__main__":
    print("ML-Based Voice Detection Training Script")
    print("=" * 60)
    print()
    print("To train the model:")
    print("1. Create folder structure:")
    print("   training_data/")
    print("     human/  (put human voice MP3s here)")
    print("     ai/     (put AI voice MP3s here)")
    print()
    print("2. Collect at least 20-50 samples of each type")
    print()
    print("3. Run:")
    print("   python app_ml.py")
    print()
    print("4. Copy model.pkl and scaler.pkl to your deployment")
    print()
    print("5. Update app.py to use ml_detect_ai_voice()")
    print()
    print("=" * 60)
    
    # Check if training data exists
    if os.path.exists('training_data'):
        response = input("\nFound training_data folder. Train model now? (y/n): ")
        if response.lower() == 'y':
            train_model('training_data')
            print("\nModel trained successfully!")
            print("You can now use this model in your API.")
    else:
        print("\nNo training_data folder found.")
        print("Create the folder structure and add samples, then run this script again.")
