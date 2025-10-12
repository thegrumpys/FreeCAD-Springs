import FreeCAD
from pathlib import Path

from .. import Utils as CoreUtils
from ..ViewProviderSpring import ViewProviderSpring
from . import Utils as SpringUtils


ENDTYPES = CoreUtils.load_end_type_table(Path(__file__).parent / "endtypes.json")


class ExtensionSpring:
    def __init__(self, obj):
        CoreUtils.add_property(obj, "OuterDiameterAtFree", 20.0, "App::PropertyFloat", "Independent")
        CoreUtils.add_property(obj, "WireDiameter", 2.0, "App::PropertyFloat", "Independent")
        CoreUtils.add_property(obj, "CoilsTotal", 10, "App::PropertyFloat", "Independent")
        CoreUtils.add_property(obj, "LengthAtFree", 25.0, "App::PropertyFloat", "Independent")

        CoreUtils.add_property(obj, "Pitch", 2.5, "App::PropertyFloat", "Dependent")
        obj.setEditorMode("Pitch", 1)
        CoreUtils.add_property(obj, "Rate", 0.0, "App::PropertyFloat", "Dependent")
        obj.setEditorMode("Rate", 1)

#        CoreUtils.add_property(obj, "EndType", "", "App::PropertyEnumeration", "Global")
        CoreUtils.add_property(obj, "InactiveCoils", 0.0, "App::PropertyFloat", "Global")
        obj.setEditorMode("InactiveCoils", 1)
        CoreUtils.add_property(obj, "EndDiameter", 0.0, "App::PropertyFloat", "Global")
        obj.setEditorMode("EndDiameter", 1)
        CoreUtils.add_property(obj, "HookDeflectionAllowance", 0.0, "App::PropertyFloat", "Global")
        obj.setEditorMode("HookDeflectionAllowance", 1)
        CoreUtils.add_property(obj, "TorsionModulus", SpringUtils.MUSIC_WIRE_SHEAR_MODULUS, "App::PropertyFloat", "Global")

        selected = CoreUtils.ensure_end_type_properties(obj, ENDTYPES)
        CoreUtils.apply_end_type_properties(obj, ENDTYPES, selected)
        obj.Proxy = self
        ViewProviderSpring(obj.ViewObject)
        SpringUtils.update_properties(obj)

    def execute(self, obj):
        radius = obj.OuterDiameterAtFree / 2.0
        wire_radius = obj.WireDiameter / 2.0
        obj.Shape = CoreUtils.helix_solid(radius, obj.Pitch, obj.LengthAtFree, wire_radius)
        SpringUtils.update_properties(obj)

    def onChanged(self, obj, prop):
        if prop in {"OuterDiameterAtFree", "WireDiameter", "CoilsTotal"}:
            SpringUtils.update_properties(obj)
        if prop == "EndType":
            selection = getattr(obj, "EndType", None)
            if isinstance(selection, (list, tuple)):
                selection = selection[0] if selection else None
            CoreUtils.apply_end_type_properties(obj, ENDTYPES, selection)
            SpringUtils.update_properties(obj)


def make():
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return None
    obj = doc.addObject("Part::FeaturePython", "ExtensionSpring")
    ExtensionSpring(obj)
    doc.recompute()
    return obj
