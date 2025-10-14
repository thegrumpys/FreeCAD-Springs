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
    if obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) == 1:
        obj.MaterialType = MUSIC_WIRE_MATERIAL_TYPE
        obj.ASTMFedSpec = MUSIC_WIRE_ASTM_FS + "/" + MUSIC_WIRE_FEDSPEC
        if obj.HotFactorKh < 1.0:
            obj.Process = "Hot Wound"
        else :
            obj.Process = "Cold Coiled"
        obj.Density = MUSIC_WIRE_DENSITY
        obj.TorsionModulus =  MUSIC_WIRE_SHEAR_MODULUS
    elif obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) == 2:
        pass #tbd
    else: # obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) == 3
        pass #tbd

#def cyclelife_calculation(material_type, life_category, spring_type, tensile, stress_at_deflection1, stress_at_deflection1) -> float:
#    var i
#    var j
#    var pntc
#    var sterm
#    var temp
#    var idxoffset
#    var snx = [
#    var sny = [7.0, 6.0, 5.0, 4.0 // Powers of 10: 10,000,000, 1,000,000, 100,000, 10,000 cycles
#    var m_tab
#    var result
#    if (Material_File === "mat_metric.json") {
#        m_tab = require('../mat_metric.json')
#    } else {
#        m_tab = require('../mat_us.json')
#    }
#    if (st_code === 3) {
#        temp = tensile
#    } else {
#        temp = 0.67 * tensile
#    }
#    const smallnum = 1.0e-7
#    var temp_stress_1 = temp - stress_1
#    if (temp_stress_1 < smallnum) temp_stress_1 = smallnum
#    var temp_stress_2 = temp - stress_2
#    if (temp_stress_2 < smallnum) temp_stress_2 = smallnum
#    var ratio = temp_stress_2 / temp_stress_1
#    pntc = stress_2 - stress_1 * ratio
#    if (pntc < smallnum) pntc = smallnum
#    if (cl_idx < 5) { // Is Life Catagory Not Peened?
#        j = 0
#    } else { // Else Shot Peened
#        j = 3
#    }
#    for (i = 0 i <= 3 i++) {
#        idxoffset = 3 - i + j
#        if (j > 0 && idxoffset === 3) { // If Shot Peened and
#            idxoffset = 0
#        }
#        if (st_code === 3) { // Is it Torsion?
#            snx[i = 0.01 * m_tab[mat_idx[mo.ptb1+idxoffset * tensile
#        } else {
#            snx[i = 0.01 * m_tab[mat_idx[mo.pte1+idxoffset * tensile
#        }
#    }
#    if (pntc < snx[0) { // Is point after the table?
#        sterm = (sny[1 - sny[0) / (snx[1 - snx[0)
#        temp = sterm * (pntc - snx[0) + sny[0
#        result =  Math.pow(10.0, temp)
#        return(result)
#    }
#    // Look for the point in the table
#    for (i = 1 i <= 3 i++) {
#        if (pntc < snx[i) {
#          j = i - 1
#          sterm = (sny[i - sny[j) / (snx[i - snx[j)
#          temp = sterm * (pntc - snx[j) + sny[j
#          result = Math.pow(10.0, temp)
#          return result
#        }
#    }
#    sterm = (sny[3 - sny[2) / (snx[3 - snx[2)
#    temp = sterm * (pntc - snx[3) + sny[3
#    result =  Math.pow(10.0, temp)
#    return result

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
    if obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) == 1:
        obj.Tensile = obj.slope_term * (math.log10(obj.WireDiameter) - obj.const_term) + obj.tensile_010
    elif obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) <= 2:
        obj.StressLimitEndurance = obj.Tensile * obj.PercentTensileEndurance / 100.0
        obj.StressLimitStatic  = obj.Tensile * obj.PercentTensileStatic  / 100.0
    if obj.StressAtDeflection2 > 0.0:
        obj.FactorOfSafetyAtDeflection2 = obj.StressLimitStatic / obj.StressAtDeflection2
    else:
        obj.FactorOfSafetyAtDeflection2 = 1.0
    if obj.StressAtSolid > 0.0:
        obj.FactorOfSafetyAtSolid = obj.StressLimitStatic / obj.StressAtSolid
    else:
        obj.FactorOfSafetyAtSolid = 1.0
    stress_average = (obj.StressAtDeflection1 + obj.StressAtDeflection2) / 2.0
    stress_range = (obj.StressAtDeflection2 - obj.StressAtDeflection1) / 2.0
    se2 = obj.StressLimitEndurance / 2.0
    obj.FactorOfSafetyAtCycleLife =  obj.StressLimitStatic / (kc * stress_range * (obj.StressLimitStatic - se2) / se2 + stress_average)
    if obj.getEnumeration("PropCalcMethod").index(obj.PropCalcMethod) == 1 and obj.Material_Type != 0:
#        obj.CycleLife = cyclelife_calculation(obj.MaterialType, obj.LifeCategory, 1, obj.Tensile, obj.StressAtDeflection1, obj.StressAtDeflection2)
        obj.Cycle_Life = 0.0
    else:
        obj.Cycle_Life = 0.0
    sq1 = obj.LengthAtFree
    sq2 = obj.CoilsTotal * math.pi * obj.MeanDiameter
    wire_len_t = math.sqrt(sq1 * sq1 + sq2 * sq2)
    if obj.getEnumeration("EndType").index(obj.EndType) == 5:
        wire_len_t = wire_len_t - 3.926 * obj.WireDiameter
    obj.Weight = obj.Density * (math.pi * obj.WireDiameter * obj.WireDiameter / 4.0) * wire_len_t
    if obj.LengthAtFree > obj.LengthAtSolid:
        obj.PercentAvailableDeflection = 100.0 * obj.Deflection2 / (obj.LengthAtFree - obj.LengthAtSolid)
        if obj.LengthAtFree < obj.LengthAtSolid + obj.WireDiameter:
            temp = 100.0 * obj.Deflection2 / obj.WireDiameter + 10000.0 * (obj.LengthAtSolid + obj.WireDiameter - obj.LengthAtFree)
            if temp < obj.PercentAvailableDeflection:
                obj.PercentAvailableDeflection = temp
    else:
        obj.PercentAvailableDeflection = 100.0 * obj.Deflection2 / obj.WireDiameter + 10000.0 * (obj.LengthAtSolid + obj.WireDiameter - obj.LengthAtFree)
    obj.Energy = 0.5 * obj.Rate * (obj.Deflection2 * obj.Deflection2 - obj.Deflection1 * obj.Deflection1)

    #=====================================
