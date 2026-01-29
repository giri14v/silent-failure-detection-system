from typing import List, Dict

# This must match the feature order used to train model.pkl
REQUIRED_FEATURES = ["feature_1", "feature_2", "feature_3"]

FEATURE_RANGES = {
    "feature_1": (0, 100),
    "feature_2": (0, 1),
    "feature_3": (0, 1000),
}


class ValidationError(Exception):
    pass


def validate_input(payload: Dict) -> List[float]:
    """
    Validate incoming request payload and return ordered feature vector.
    Raises ValidationError if anything is invalid.
    """
    features = []

    for feature in REQUIRED_FEATURES:
        if feature not in payload:
            raise ValidationError(f"Missing required feature: {feature}")

        value = payload[feature]

        if value is None:
            raise ValidationError(f"Null value for feature: {feature}")

        if not isinstance(value, (int, float)):
            raise ValidationError(f"Invalid type for {feature}: {type(value)}")

        min_val, max_val = FEATURE_RANGES[feature]
        if not (min_val <= value <= max_val):
            raise ValidationError(f"{feature} out of range: {value}")

        features.append(float(value))

    return features