import FreeCAD
from .. import Utils
from ..ViewProviderSpring import ViewProviderSpring

class Spring:
    def __init__(self, obj):
        Utils.add_property(obj, "MeanDiameter", 20.0)
        Utils.add_property(obj, "WireDiameter", 2.0)
        Utils.add_property(obj, "Pitch", 2.5)
        Utils.add_property(obj, "NumberOfTurns", 10)
        Utils.add_property(obj, "Height", 25.0)
        obj.Proxy = self
        ViewProviderSpring(obj.ViewObject)

    def execute(self, obj):
        radius = obj.MeanDiameter / 2.0
        wire_radius = obj.WireDiameter / 2.0
        obj.Shape = Utils.helix_solid(radius, obj.Pitch, obj.Height, wire_radius)


def make():
    doc = FreeCAD.ActiveDocument or FreeCAD.newDocument()
    obj = doc.addObject("Part::FeaturePython", "TorsionSpring")
    Spring(obj)
    doc.recompute()
    return obj
