import FreeCAD, FreeCADGui
from PySide2 import QtWidgets

class SpringsPreferencePage:
    def __init__(self):
        self.form = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(self.form)
        self.default_diameter = QtWidgets.QDoubleSpinBox()
        self.default_diameter.setRange(1.0, 100.0)
        self.default_diameter.setValue(20.0)
        layout.addRow("Default mean diameter (mm):", self.default_diameter)

        self.default_wire = QtWidgets.QDoubleSpinBox()
        self.default_wire.setRange(0.1, 10.0)
        self.default_wire.setValue(2.0)
        layout.addRow("Default wire diameter (mm):", self.default_wire)

        self.default_pitch = QtWidgets.QDoubleSpinBox()
        self.default_pitch.setRange(0.1, 10.0)
        self.default_pitch.setValue(2.5)
        layout.addRow("Default pitch (mm):", self.default_pitch)

        self.default_height = QtWidgets.QDoubleSpinBox()
        self.default_height.setRange(1.0, 200.0)
        self.default_height.setValue(25.0)
        layout.addRow("Default height (mm):", self.default_height)

    def saveSettings(self):
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Springs")
        p.SetFloat("MeanDiameter", self.default_diameter.value())
        p.SetFloat("WireDiameter", self.default_wire.value())
        p.SetFloat("Pitch", self.default_pitch.value())
        p.SetFloat("Height", self.default_height.value())

    def loadSettings(self):
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Springs")
        self.default_diameter.setValue(p.GetFloat("MeanDiameter", 20.0))
        self.default_wire.setValue(p.GetFloat("WireDiameter", 2.0))
        self.default_pitch.setValue(p.GetFloat("Pitch", 2.5))
        self.default_height.setValue(p.GetFloat("Height", 25.0))

FreeCADGui.addPreferencePage(SpringsPreferencePage, "Springs")
