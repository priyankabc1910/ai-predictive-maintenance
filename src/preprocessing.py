import numpy as np


def prepare_lstm_sequence(
    engine_data,
    sensor_columns,
    scaler,
    window_size=30
):
    """
    Prepare the latest sensor window for LSTM inference.
    """

    engine_data = engine_data.sort_values("cycle")

    if len(engine_data) < window_size:
        raise ValueError(
            f"Engine has fewer than {window_size} cycles."
        )

    latest_data = engine_data[
        sensor_columns
    ].tail(window_size)

    scaled_window = scaler.transform(
        latest_data
    )

    sequence = np.expand_dims(
        scaled_window,
        axis=0
    )

    return sequence