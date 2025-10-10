import FreeCAD
from pathlib import Path

from .. import Utils
from ..ViewProviderSpring import ViewProviderSpring


END_TYPES = Utils.load_end_type_table(Path(__file__).parent / "endtypes.json")


class TorsionSpring:
    def __init__(self, obj):
        Utils.add_property(obj, "MeanDiameter", 20.0)
        Utils.add_property(obj, "WireDiameter", 2.0)
        Utils.add_property(obj, "Pitch", 2.5)
        Utils.add_property(obj, "NumberOfTurns", 10)
        Utils.add_property(obj, "Height", 25.0)
        selected = Utils.ensure_end_type_properties(obj, END_TYPES)
        Utils.apply_end_type_properties(obj, END_TYPES, selected)
        obj.Proxy = self
        ViewProviderSpring(obj.ViewObject)

    def execute(self, obj):
        radius = obj.MeanDiameter / 2.0
        wire_radius = obj.WireDiameter / 2.0
        obj.Shape = Utils.helix_solid(radius, obj.Pitch, obj.Height, wire_radius)

    def onChanged(self, obj, prop):
        if prop == "EndType":
            selection = getattr(obj, "EndType", None)
            if isinstance(selection, (list, tuple)):
                selection = selection[0] if selection else None
            Utils.apply_end_type_properties(obj, END_TYPES, selection)


def make():
    doc = FreeCAD.ActiveDocument or FreeCAD.newDocument()
    obj = doc.addObject("Part::FeaturePython", "TorsionSpring")
    TorsionSpring(obj)
    doc.recompute()
    return obj
