"""Utilities specific to compression springs."""

from __future__ import annotations

MUSIC_WIRE_SHEAR_MODULUS = 79.3e9  # Pascals


def _as_float(value, default):
    try:
        candidate = getattr(value, "Value", value)
        return float(candidate)
    except (TypeError, ValueError):
        return float(default)


def update_properties(obj) -> None:
    """Update properties based on the object's properties."""

    rate = 0.0

    try:
        outer = float(obj.OuterDiameterAtFree)
        wire = float(obj.WireDiameter)
        coils = float(obj.CoilsTotal)
        shear_modulus = _as_float(getattr(obj, "TorsionModulus", MUSIC_WIRE_SHEAR_MODULUS), MUSIC_WIRE_SHEAR_MODULUS)
    except (AttributeError, TypeError, ValueError):
        obj.Rate = rate
        return

    mean_diameter = outer - wire
    if mean_diameter <= 0.0 or wire <= 0.0 or coils <= 0.0 or shear_modulus <= 0.0:
        obj.Rate = rate
        return

    wire_m = wire / 1000.0
    mean_m = mean_diameter / 1000.0
    rate_n_per_m = (shear_modulus * wire_m**4) / (8.0 * coils * (mean_m**3))
    rate = rate_n_per_m / 1000.0
    obj.Rate = rate
