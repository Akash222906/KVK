import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

CROPS = [
    'Rice (Aman)', 'Rice (Boro)', 'Rice (Aus)', 'Jute', 'Potato',
    'Mustard', 'Wheat', 'Vegetables', 'Maize', 'Sesame',
    'Groundnut', 'Sugarcane', 'Tomato', 'Brinjal', 'Onion'
]

CROP_PARAMS = {
    'Rice (Aman)':   {'N': (60,90),  'P': (30,50), 'K': (30,50), 'pH': (5.5,7.0), 'temp': (24,32), 'rain': (150,250), 'hum': (70,90)},
    'Rice (Boro)':   {'N': (80,120), 'P': (40,60), 'K': (40,60), 'pH': (5.5,7.0), 'temp': (20,30), 'rain': (100,200), 'hum': (65,85)},
    'Rice (Aus)':    {'N': (50,80),  'P': (25,45), 'K': (25,45), 'pH': (5.5,7.0), 'temp': (26,34), 'rain': (120,220), 'hum': (70,90)},
    'Jute':          {'N': (40,70),  'P': (20,40), 'K': (20,40), 'pH': (6.0,7.5), 'temp': (25,35), 'rain': (150,250), 'hum': (75,95)},
    'Potato':        {'N': (100,150),'P': (60,90), 'K': (80,120),'pH': (5.0,6.5), 'temp': (15,22), 'rain': (50,120),  'hum': (70,85)},
    'Mustard':       {'N': (40,80),  'P': (20,40), 'K': (20,40), 'pH': (6.0,7.5), 'temp': (10,20), 'rain': (30,80),   'hum': (50,70)},
    'Wheat':         {'N': (80,120), 'P': (40,60), 'K': (30,50), 'pH': (6.0,7.5), 'temp': (10,22), 'rain': (40,100),  'hum': (50,70)},
    'Vegetables':    {'N': (80,120), 'P': (50,80), 'K': (60,90), 'pH': (5.5,7.0), 'temp': (18,28), 'rain': (60,150),  'hum': (60,80)},
    'Maize':         {'N': (100,150),'P': (50,80), 'K': (40,70), 'pH': (5.5,7.5), 'temp': (20,30), 'rain': (80,180),  'hum': (60,80)},
    'Sesame':        {'N': (30,60),  'P': (20,40), 'K': (20,40), 'pH': (5.5,7.5), 'temp': (25,35), 'rain': (50,120),  'hum': (50,70)},
    'Groundnut':     {'N': (20,40),  'P': (40,70), 'K': (40,70), 'pH': (5.5,7.0), 'temp': (25,32), 'rain': (80,150),  'hum': (55,75)},
    'Sugarcane':     {'N': (120,180),'P': (60,90), 'K': (80,120),'pH': (6.0,7.5), 'temp': (25,35), 'rain': (150,250), 'hum': (60,80)},
    'Tomato':        {'N': (100,150),'P': (60,90), 'K': (80,120),'pH': (5.5,7.0), 'temp': (18,27), 'rain': (60,120),  'hum': (60,75)},
    'Brinjal':       {'N': (80,120), 'P': (40,70), 'K': (50,80), 'pH': (5.5,7.0), 'temp': (22,30), 'rain': (60,130),  'hum': (60,80)},
    'Onion':         {'N': (60,100), 'P': (40,70), 'K': (50,80), 'pH': (6.0,7.5), 'temp': (13,24), 'rain': (35,100),  'hum': (50,70)},
}

le = LabelEncoder()
le.fit(CROPS)

def generate_training_data(n=3000):
    np.random.seed(42)
    X, y = [], []
    per_crop = n // len(CROPS)
    for crop, p in CROP_PARAMS.items():
        for _ in range(per_crop):
            N    = np.random.uniform(*p['N'])
            P    = np.random.uniform(*p['P'])
            K    = np.random.uniform(*p['K'])
            pH   = np.random.uniform(*p['pH'])
            temp = np.random.uniform(*p['temp'])
            rain = np.random.uniform(*p['rain'])
            hum  = np.random.uniform(*p['hum'])
            X.append([N, P, K, pH, temp, rain, hum])
            y.append(crop)
    return np.array(X), np.array(y)

def generate_yield_data(n=2000):
    np.random.seed(99)
    X, y = [], []
    yields = {
        'Rice (Aman)': (25,40), 'Rice (Boro)': (35,55), 'Rice (Aus)': (20,35),
        'Jute': (15,28), 'Potato': (100,200), 'Mustard': (8,18),
        'Wheat': (20,40), 'Vegetables': (80,180), 'Maize': (30,55),
        'Sesame': (5,12), 'Groundnut': (12,22), 'Sugarcane': (300,600),
        'Tomato': (100,200), 'Brinjal': (80,160), 'Onion': (70,140),
    }
    for crop, (lo, hi) in yields.items():
        for _ in range(n // len(CROPS)):
            p = CROP_PARAMS[crop]
            feat = [
                np.random.uniform(*p['N']),
                np.random.uniform(*p['P']),
                np.random.uniform(*p['K']),
                np.random.uniform(*p['pH']),
                np.random.uniform(*p['temp']),
                np.random.uniform(*p['rain']),
                np.random.uniform(*p['hum']),
                le.transform([crop])[0]
            ]
            X.append(feat)
            y.append(np.random.uniform(lo, hi))
    return np.array(X), np.array(y)

def train_models():
    crop_path  = os.path.join(MODEL_DIR, 'crop_recommender.pkl')
    yield_path = os.path.join(MODEL_DIR, 'yield_predictor.pkl')
    le_path    = os.path.join(MODEL_DIR, 'label_encoder.pkl')

    X_crop, y_crop = generate_training_data()
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_crop, y_crop)
    joblib.dump(clf, crop_path)

    X_yield, y_yield = generate_yield_data()
    reg = GradientBoostingRegressor(n_estimators=100, random_state=42)
    reg.fit(X_yield, y_yield)
    joblib.dump(reg, yield_path)
    joblib.dump(le, le_path)
    print("Models saved successfully.")

def load_models():
    crop_path  = os.path.join(MODEL_DIR, 'crop_recommender.pkl')
    yield_path = os.path.join(MODEL_DIR, 'yield_predictor.pkl')
    le_path    = os.path.join(MODEL_DIR, 'label_encoder.pkl')
    if not os.path.exists(crop_path):
        train_models()
    clf = joblib.load(crop_path)
    reg = joblib.load(yield_path)
    le2 = joblib.load(le_path)
    return clf, reg, le2

def recommend_crops(N, P, K, pH, temp, rain, hum):
    clf, _, _ = load_models()
    feat = np.array([[N, P, K, pH, temp, rain, hum]])
    proba = clf.predict_proba(feat)[0]
    top3_idx = np.argsort(proba)[-3:][::-1]
    results = []
    for i in top3_idx:
        results.append({'crop': clf.classes_[i], 'confidence': round(float(proba[i]) * 100, 1)})
    return results

def predict_yield(N, P, K, pH, temp, rain, hum, crop):
    _, reg, le2 = load_models()
    try:
        crop_enc = le2.transform([crop])[0]
    except:
        crop_enc = 0
    feat = np.array([[N, P, K, pH, temp, rain, hum, crop_enc]])
    return round(float(reg.predict(feat)[0]), 2)

def assess_pest_risk(temp, hum, crop):
    risks = []
    if temp > 28 and hum > 75:
        risks.append({'pest': 'Brown Plant Hopper (BPH)', 'risk': 'High', 'treatment': 'Apply Imidacloprid 17.8 SL @ 0.5 ml/L water'})
    if temp > 25 and hum > 70:
        risks.append({'pest': 'Stem Borer', 'risk': 'Medium', 'treatment': 'Apply Chlorpyrifos 20 EC @ 2.5 ml/L water'})
    if temp < 18 and hum > 80:
        risks.append({'pest': 'Blast Disease', 'risk': 'High', 'treatment': 'Spray Tricyclazole 75 WP @ 0.6 g/L water'})
    if hum > 85:
        risks.append({'pest': 'Sheath Blight', 'risk': 'Medium', 'treatment': 'Apply Hexaconazole 5 SC @ 2 ml/L water'})
    if not risks:
        risks.append({'pest': 'No major pest risk detected', 'risk': 'Low', 'treatment': 'Continue regular field monitoring'})
    return risks
