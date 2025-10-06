import FreeCADGui as Gui
from Features import CompressionSpring

class CmdCompressionSpring:
    """Command to create a parametric compression spring"""

    def GetResources(self):
        """Defines icon, tooltip, and menu text"""
        return {
            "Pixmap": "compression.svg",  # must exist in Resources/icons/
            "MenuText": "Compression Spring",
            "ToolTip": "Create a parametric compression spring",
        }

    def Activated(self):
        """What happens when user clicks the command"""
        CompressionSpring.make()

    def IsActive(self):
        """Keep the command always available"""
        return True

def register():
    """Registers this command with FreeCAD"""
    Gui.addCommand("Springs_CreateCompression", CmdCompressionSpring())
