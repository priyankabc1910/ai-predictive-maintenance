from dataclasses import dataclass


@dataclass
class PredictionResult:
    engine_id: int
    rul: float
    health_score: float
    risk_level: str
    recommendation: str