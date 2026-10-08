from dataclasses import dataclass


@dataclass
class PredictionResult:
    engine_id: int
    rul: float
    health_score: float
    risk_level: str
    recommendation: str

@dataclass
class ModelMetadata:
    name: str
    model_type: str
    dataset: str
    target: str
    version: str
    artifact_path: str
    description: str