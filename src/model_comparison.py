from typing import Dict, List


REQUIRED_MODEL_FIELDS = {
    "model",
    "mae",
    "rmse",
}


def validate_model_result(model_result: Dict) -> None:
    """
    Validate a single model evaluation result.
    """

    missing_fields = (
        REQUIRED_MODEL_FIELDS
        - model_result.keys()
    )

    if missing_fields:
        raise ValueError(
            f"Missing required model fields: "
            f"{sorted(missing_fields)}"
        )

    if model_result["mae"] < 0:
        raise ValueError("MAE cannot be negative.")

    if model_result["rmse"] < 0:
        raise ValueError("RMSE cannot be negative.")

    if model_result["rmse"] < model_result["mae"]:
        raise ValueError(
            "RMSE cannot be lower than MAE."
        )


def compare_models(
    model_results: List[Dict],
) -> List[Dict]:
    """
    Rank models by MAE, with lower MAE considered better.
    """

    if not model_results:
        return []

    for model_result in model_results:
        validate_model_result(model_result)

    ranked = sorted(
        model_results,
        key=lambda item: item["mae"],
    )

    results = []

    for rank, model in enumerate(
        ranked,
        start=1,
    ):
        result = dict(model)
        result["rank"] = rank
        results.append(result)

    return results


def get_best_model(
    model_results: List[Dict],
) -> Dict:
    """
    Return the model with the lowest MAE.
    """

    ranked = compare_models(model_results)

    if not ranked:
        raise ValueError(
            "model_results cannot be empty."
        )

    return ranked[0]