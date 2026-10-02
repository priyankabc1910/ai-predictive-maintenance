from pydantic import BaseModel


class PredictionResponse(BaseModel):
    machine_id: str
    engine_id: int
    rul: float
    health_score: float
    risk_level: str
    recommendation: str