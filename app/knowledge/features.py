import json
from pathlib import Path


features_path = Path(__file__).parent / "features.json"
with open(features_path, 'r') as f:
    FEATURES = json.load(f)


def get_feature_list():
    """Returns a list of all available feature names."""
    return list(FEATURES.keys())

def get_feature_details(feature_name: str):
    """Returns the complete details for a specific feature."""
    return FEATURES.get(feature_name)

def get_feature_description(feature_name: str):
    """Returns only the description for a specific feature."""
    feature = FEATURES.get(feature_name)
    return feature.get('description') if feature else None

def get_feature_subfeatures(feature_name: str):
    """Returns the sub-features list for a specific feature."""
    feature = FEATURES.get(feature_name)
    return feature.get('sub_features', []) if feature else []

def get_feature_url(feature_name: str):
    """Returns the URL for a specific feature."""
    feature = FEATURES.get(feature_name)
    return feature.get('url') if feature else None

def is_valid_feature(feature_name: str) -> bool:
    """Check if a feature name exists in the features list."""
    return feature_name in FEATURES
