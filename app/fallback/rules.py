"""
Deterministic fallback logic.

This module MUST NOT:
- Call ML models
- Use probabilities
- Depend on LLMs
- Access monitoring metrics

It only receives features and returns safe outputs.
"""

def apply_fallback(features):
    """
    Very conservative rule-based behavior.
    This is intentionally simple and safe.
    """

    # Example: binary classification style
    # We always return a neutral / low-risk decision
    prediction = "SAFE"
    confidence = 1.0

    return prediction, confidence