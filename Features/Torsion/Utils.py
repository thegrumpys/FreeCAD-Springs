"""Utilities specific to torsion springs."""

from __future__ import annotations

MUSIC_WIRE_YOUNG_MODULUS = 207e9  # Pascals

def _as_float(value, default):
    try:
        candidate = getattr(value, "Value", value)
        return float(candidate)
    except (TypeError, ValueError):
        return float(default)

def update_globals(obj) -> None:
    """Update global properties based on the object's global properties."""


def update_properties(obj) -> None:
    """Update properties based on the object's properties."""

    rate = 0.0

    try:
        outer = float(obj.OutsideDiameterAtFree)
        wire = float(obj.WireDiameter)
        coils = float(obj.CoilsTotal)
        young_modulus = _as_float(getattr(obj, "ElasticModulus", MUSIC_WIRE_YOUNG_MODULUS), MUSIC_WIRE_YOUNG_MODULUS)
    except (AttributeError, TypeError, ValueError):
        obj.Rate = rate
        return

    mean_diameter = outer - wire
    if mean_diameter <= 0.0 or wire <= 0.0 or coils <= 0.0 or young_modulus <= 0.0:
        obj.Rate = rate
        return

    wire_m = wire / 1000.0
    mean_m = mean_diameter / 1000.0
    torque_per_radian = (young_modulus * wire_m**4) / (64.0 * coils * mean_m)
    rate = torque_per_radian * 1000.0
    obj.Rate = rate
