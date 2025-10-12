"""Utilities specific to torsion springs."""

from __future__ import annotations

from typing import Union

MUSIC_WIRE_YOUNG_MODULUS = 207e9  # Pascals


Number = Union[float, int]


def spring_rate(
    wire_diameter_m: Number,
    mean_diameter_m: Number,
    coils: Number,
    *,
    modulus: Number = MUSIC_WIRE_YOUNG_MODULUS,
) -> float:
    """Return the torsion spring rate in N·mm per radian."""

    try:
        d = float(wire_diameter_m)
        D = float(mean_diameter_m)
        n = float(coils)
        E = float(modulus)
    except (TypeError, ValueError):
        return 0.0

    if d <= 0.0 or D <= 0.0 or n <= 0.0 or E <= 0.0:
        return 0.0

    torque_per_radian = (E * d**4) / (64.0 * n * D)
    return torque_per_radian * 1000.0
