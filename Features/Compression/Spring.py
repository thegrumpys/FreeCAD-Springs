import FreeCAD
from pathlib import Path

from .. import Utils
from ..ViewProviderSpring import ViewProviderSpring


ENDTYPES = Utils.load_end_type_table(Path(__file__).parent / "endtypes.json")


class CompressionSpring:
    def __init__(self, obj):
        Utils.add_property(obj, "OuterDiameterAtFree", 20.0)
        Utils.add_property(obj, "WireDiameter", 2.0)
        Utils.add_property(obj, "Pitch", 2.5)
        Utils.add_property(obj, "CoilsTotal", 10)
        Utils.add_property(obj, "LengthAtFree", 25.0)
        selected = Utils.ensure_end_type_properties(obj, ENDTYPES)
        Utils.apply_end_type_properties(obj, ENDTYPES, selected)
        obj.Proxy = self
        ViewProviderSpring(obj.ViewObject)

    def execute(self, obj):
        radius = obj.OuterDiameterAtFree / 2.0
        wire_radius = obj.WireDiameter / 2.0
        obj.Shape = Utils.helix_solid(radius, obj.Pitch, obj.LengthAtFree, wire_radius)

    def onChanged(self, obj, prop):
        if prop == "EndType":
            selection = getattr(obj, "EndType", None)
            if isinstance(selection, (list, tuple)):
                selection = selection[0] if selection else None
            Utils.apply_end_type_properties(obj, ENDTYPES, selection)


def make():
    doc = FreeCAD.ActiveDocument or FreeCAD.newDocument()
    obj = doc.addObject("Part::FeaturePython", "CompressionSpring")
    CompressionSpring(obj)
    doc.recompute()
    return obj
