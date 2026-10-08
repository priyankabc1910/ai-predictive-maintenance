from pathlib import Path

from .schemas import ModelMetadata


BASE_DIR = Path(__file__).resolve().parents[1]


def get_lstm_model_metadata() -> ModelMetadata:
    return ModelMetadata(
        name="LSTM RUL Predictor",
        model_type="LSTM",
        dataset="NASA C-MAPSS FD001",
        target="RUL",
        version="1.0.0",
        artifact_path="models/lstm_rul_model_FD001.keras",
        description=(
            "Temporal deep learning model using 30-cycle windows "
            "of selected sensor measurements for RUL prediction."
        ),
    )

def get_random_forest_metadata() -> ModelMetadata:
    return ModelMetadata(
        name="Random Forest RUL Predictor",
        model_type="RandomForest",
        dataset="NASA C-MAPSS FD001",
        target="RUL",
        version="1.0.0",
        artifact_path="models/best_rul_model_FD001.pkl",
        description=(
            "Tree-based regression baseline using engineered "
            "sensor features for RUL prediction."
        ),
    )


def get_xgboost_metadata() -> ModelMetadata:
    return ModelMetadata(
        name="XGBoost RUL Predictor",
        model_type="XGBoost",
        dataset="NASA C-MAPSS FD001",
        target="RUL",
        version="1.0.0",
        artifact_path="models/xgb_rul_model_FD001.pkl",
        description=(
            "Gradient boosting regression model using engineered "
            "sensor features for RUL prediction."
        ),
    )

def get_registered_models() -> list[ModelMetadata]:
    return [
        get_lstm_model_metadata(),
        get_random_forest_metadata(),
        get_xgboost_metadata(),
    ]