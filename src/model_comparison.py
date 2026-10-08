from typing import Dict, List


def compare_models(model_results: List[Dict]) -> List[Dict]:
    """
    Rank models by MAE, with lower MAE considered better.
    """

    if not model_results:
        return []

    ranked = sorted(
        model_results,
        key=lambda item: item["mae"],
    )

    results = []

    for rank, model in enumerate(ranked, start=1):
        result = dict(model)
        result["rank"] = rank
        results.append(result)

    return results


def get_best_model(model_results: List[Dict]) -> Dict:
    """
    Return the model with the lowest MAE.
    """

    ranked = compare_models(model_results)

    if not ranked:
        raise ValueError("model_results cannot be empty.")

    return ranked[0]