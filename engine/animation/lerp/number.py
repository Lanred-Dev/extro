def lerpNumber(start: float, end: float, progress: float) -> float:
    """Lerp between a start and end number at x."""
    return start + (end - start) * progress
