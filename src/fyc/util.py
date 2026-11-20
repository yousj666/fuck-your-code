"""Tiny shared helpers for the fuck-your-code package."""


def clamp(value, low=0.0, high=100.0):
    """Clamp a score into the inclusive range between low and high."""
    return max(low, min(high, value))
