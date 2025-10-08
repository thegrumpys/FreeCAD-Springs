import FreeCADGui
from Springs.Dialogs.SpringInfoDialog import SpringInfoDialog

class DisplaySpringInfo:
    def GetResources(self):
        return {
            'Pixmap': 'SpringInfo.svg',
            'MenuText': 'Spring Info',
            'ToolTip': 'Show analytic spring information for the selected object'
        }

    def Activated(self):
        SpringInfoDialog.show_for_selected()

    def IsActive(self):
        return bool(FreeCADGui.Selection.getSelection())

FreeCADGui.addCommand('Springs_DisplaySpringInfo', DisplaySpringInfo())
