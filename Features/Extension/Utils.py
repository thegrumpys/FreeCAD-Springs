"""Utilities specific to extension springs."""

from __future__ import annotations

from typing import Union

MUSIC_WIRE_SHEAR_MODULUS = 79.3e9  # Pascals


Number = Union[float, int]


def spring_rate(
    wire_diameter_m: Number,
    mean_diameter_m: Number,
    coils: Number,
    *,
    modulus: Number = MUSIC_WIRE_SHEAR_MODULUS,
) -> float:
    """Return the extension spring rate in N/mm."""

    try:
        d = float(wire_diameter_m)
        D = float(mean_diameter_m)
        n = float(coils)
        G = float(modulus)
    except (TypeError, ValueError):
        return 0.0

    if d <= 0.0 or D <= 0.0 or n <= 0.0 or G <= 0.0:
        return 0.0

    rate_n_per_m = (G * d**4) / (8.0 * n * (D**3))
    return rate_n_per_m / 1000.0
