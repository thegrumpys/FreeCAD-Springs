import FreeCADGui as Gui
from Features import ExtensionSpring

class CreateExtensionSpring:
    """Command to create a parametric extension spring"""

    def GetResources(self):
        """Defines icon, tooltip, and menu text"""
        return {
            "Pixmap": "extension.svg",  # must exist in Resources/icons/
            "MenuText": "Extension Spring",
            "ToolTip": "Create a parametric extension spring",
        }

    def Activated(self):
        """What happens when user clicks the command"""
        ExtensionSpring.make()

    def IsActive(self):
        """Keep the command always available"""
        return True

def register():
    """Registers this command with FreeCAD"""
    Gui.addCommand("Springs_CreateExtensionSpring", CreateExtensionSpring())
