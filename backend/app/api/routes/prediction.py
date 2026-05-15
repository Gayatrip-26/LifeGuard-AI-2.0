from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "service": "Prediction Service",
        "status": "running"
    }

@app.post("/predict")
def predict(data: dict):

    score = 20

    if data.get("heart_rate", 0) > 100:
        score += 30

    if data.get("stress_level", 0) > 70:
        score += 25

    if data.get("sleep_hours", 0) < 5:
        score += 20

    risk = "Low"

    if score > 70:
        risk = "High"
    elif score > 40:
        risk = "Medium"

    return {
        "risk_score": score,
        "risk_level": risk,
        "prediction": "Demo prediction generated for public showcase."
    }
