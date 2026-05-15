from fastapi import APIRouter

router = APIRouter()

@router.post("/ai/query")
def ai_query(data: dict):

    heart_rate = data.get("heart_rate", 0)
    temperature = data.get("temperature", 0)
    stress = data.get("stress_level", 0)
    sleep = data.get("sleep_hours", 0)

    risk = "Low"

    if heart_rate > 110 or temperature > 39:
        risk = "High"

    elif stress > 70 or sleep < 5:
        risk = "Medium"

    return {
        "status": "success",
        "risk_level": risk,
        "health_summary": f"Patient health status detected as {risk} risk.",
        "possible_issue": "Stress or irregular health patterns detected.",
        "recommendation": [
            "Maintain healthy sleep schedule",
            "Drink sufficient water",
            "Monitor heart rate regularly"
        ],
        "ai_explanation": "This is a demo AI explanation generated for portfolio showcase purposes."
    }
