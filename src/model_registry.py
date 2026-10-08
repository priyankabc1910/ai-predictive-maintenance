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


def get_registered_models() -> list[ModelMetadata]:
    return [
        get_lstm_model_metadata(),
    ]