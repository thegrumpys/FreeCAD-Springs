"""Utilities specific to compression springs."""

from __future__ import annotations
import math

#    ["matnam",        "astm_fs",   "fedspec","Density",  "ee",   "gg", "kh","t010","t400","pte1","pte2","pte3","pte4","pte6","pte7","pte8","ptb1","ptb2","ptb3","ptb4","ptb6","ptb7","ptb8", "ptb1sr", "ptb1nosr", "ptb2sr", "ptb3sr", "silf", "sihf", "sisr", "wire_dia_filename", "od_free_filename", "dumyc", "longnam"],
#    ["MUSIC_WIRE",      "A228",    "QQW-470",  0.00786, 207.0, 79.293, 1.00,  2.55,  1.38,    50,    36,    33,    30,    42,    39,    36,    75,    51,    47,    45,     0,     0,     0,       85,        100,       53,       50, 188.92, 310.28, 399.91, "wire_dia_metric",   "od_free_metric",       1,   "Music Wire  (all coatings) -                     ASTM A-228 "],

MUSIC_WIRE_MATERIAL_TYPE = "MUSIC_WIRE"
MUSIC_WIRE_ASTM_FS = "A228"
MUSIC_WIRE_FEDSPEC = "QQW-470"
MUSIC_WIRE_DENSITY = 0.00786
MUSIC_WIRE_ELASTIC_MODULUS = 207.0  # Pascals
MUSIC_WIRE_SHEAR_MODULUS = 79.293e9  # Pascals
MUSIC_WIRE_HOT_FACTOR_KH = 1.0  # Ratio
MUSIC_WIRE_T010 = 2.55
MUSIC_WIRE_T400 = 1.38

def _as_float(value, default):
    try:
        candidate = getattr(value, "Value", value)
        return float(candidate)
    except (TypeError, ValueError):
        return float(default)

def update_globals(obj) -> None:
    """Update global properties based on the object's global properties."""
    if obj.PropCalcMethod == "Use values from material table":
        obj.MaterialType = MUSIC_WIRE_MATERIAL_TYPE
        obj.ASTMFedSpec = MUSIC_WIRE_ASTM_FS + "/" + MUSIC_WIRE_FEDSPEC
        if obj.HotFactorKh < 1.0:
            obj.Process = "Hot Wound"
        else :
            obj.Process = "Cold Coiled"
        obj.Density = MUSIC_WIRE_DENSITY
        obj.TorsionModulus =  MUSIC_WIRE_SHEAR_MODULUS
    elif obj.PropCalcMethod == "Use Tensile & %_Tensile_...":
        pass #tbd
    else: # obj.PropCalcMethod == "Use Stress_Lim_...":
        pass #tbd

def update_properties(obj) -> None:
    """Update properties based on the object's properties."""

    obj.MeanDiameter = obj.OutsideDiameterAtFree - obj.WireDiameter
    obj.InsideDiameterAtFree = obj.MeanDiameter - obj.WireDiameter
    obj.SpringIndex = obj.MeanDiameter / obj.WireDiameter
    kc = (4.0 * obj.SpringIndex - 1.0) / (4.0 * obj.SpringIndex - 4.0)
    ks = kc + 0.615 / obj.SpringIndex
    obj.CoilsActive = obj.CoilsTotal - obj.CoilsInactive
    temp = obj.SpringIndex * obj.SpringIndex
    obj.Rate = obj.HotFactorKh * (obj.TorsionModulus / 1.0e6) * obj.MeanDiameter / (8.0 * obj.CoilsActive * temp * temp)
    obj.Deflection1 = obj.ForceAtDeflection1 / obj.Rate
    obj.Deflection2 = obj.ForceAtDeflection2 / obj.Rate
    obj.LengthAtDeflection1 = obj.LengthAtFree - obj.Deflection1
    obj.LengthAtDeflection2 = obj.LengthAtFree - obj.Deflection2
    obj.LengthStroke = obj.LengthAtDeflection1 - obj.LengthAtDeflection2
    obj.Slenderness = obj.LengthAtFree / obj.MeanDiameter
    obj.LengthAtSolid = obj.WireDiameter * (obj.CoilsTotal + obj.AddCoilsAtSolid)
    obj.ForceAtSolid = obj.Rate * (obj.LengthAtFree - obj.LengthAtSolid)
    s_f = ks * 8.0 * obj.MeanDiameter / (math.pi * obj.WireDiameter * obj.WireDiameter * obj.WireDiameter)
    obj.StressAtDeflection1 = s_f * obj.ForceAtDeflection1
    obj.StressAtDeflection2 = s_f * obj.ForceAtDeflection2
    obj.StressAtSolid = s_f * obj.ForceAtSolid
#    if obj.PropCalcMethod == "Use values from material table":
#        obj.Tensile = obj.slope_term * (math.log10(obj.WireDiameter) - obj.const_term) + obj.tensile_010
#    elif obj.PropCalcMethod == "Use values from material table":
#        pass # tbd

    #=====================================
