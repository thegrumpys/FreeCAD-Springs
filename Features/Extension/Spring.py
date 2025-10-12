import FreeCAD
from pathlib import Path

from .. import Utils as CoreUtils
from ..ViewProviderSpring import ViewProviderSpring
from . import Utils as SpringUtils


ENDTYPES = CoreUtils.load_end_type_table(Path(__file__).parent / "endtypes.json")


class ExtensionSpring:
    def __init__(self, obj):
        CoreUtils.add_property(obj, "OuterDiameterAtFree", 20.0)
        CoreUtils.add_property(obj, "WireDiameter", 2.0)
        CoreUtils.add_property(obj, "Pitch", 2.5)
        CoreUtils.add_property(obj, "CoilsTotal", 10)
        CoreUtils.add_property(obj, "LengthAtFree", 25.0)
        CoreUtils.add_property(obj, "Rate", 0.0)
        selected = CoreUtils.ensure_end_type_properties(obj, ENDTYPES)
        CoreUtils.apply_end_type_properties(obj, ENDTYPES, selected)
        obj.setEditorMode("Rate", 1)
        obj.Proxy = self
        ViewProviderSpring(obj.ViewObject)
        self._update_properties(obj)

    def execute(self, obj):
        radius = obj.OuterDiameterAtFree / 2.0
        wire_radius = obj.WireDiameter / 2.0
        obj.Shape = CoreUtils.helix_solid(radius, obj.Pitch, obj.LengthAtFree, wire_radius)
        self._update_properties(obj)

    def onChanged(self, obj, prop):
        if prop in {"OuterDiameterAtFree", "WireDiameter", "CoilsTotal"}:
            self._update_properties(obj)
        if prop == "EndType":
            selection = getattr(obj, "EndType", None)
            if isinstance(selection, (list, tuple)):
                selection = selection[0] if selection else None
            CoreUtils.apply_end_type_properties(obj, ENDTYPES, selection)
            self._update_properties(obj)

    @staticmethod
    def _update_properties(obj):
        try:
            outer = float(obj.OuterDiameterAtFree)
            wire = float(obj.WireDiameter)
            coils = float(obj.CoilsTotal)
        except (AttributeError, TypeError, ValueError):
            obj.Rate = 0.0
            return

        mean_diameter = outer - wire
        if mean_diameter <= 0 or wire <= 0 or coils <= 0:
            obj.Rate = 0.0
            return

        wire_m = wire / 1000.0
        mean_m = mean_diameter / 1000.0
        obj.Rate = SpringUtils.spring_rate(wire_m, mean_m, coils)


def make():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return None
    obj = doc.addObject("Part::FeaturePython", "ExtensionSpring")
    ExtensionSpring(obj)
    doc.recompute()
    return obj
