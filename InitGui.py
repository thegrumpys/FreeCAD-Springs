import os
import FreeCADGui as Gui

# --- Safe way to get this file's directory even if __file__ is undefined ---
try:
    MODULE_PATH = os.path.dirname(__file__)
except NameError:
    import inspect
    MODULE_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))

Gui.addIconPath(os.path.join(MODULE_PATH, "Resources", "icons"))

class SpringsWorkbench(Gui.Workbench):
    MenuText = "Springs"
    ToolTip = "Design compression, extension, and torsion springs"
    Icon = "workbench.svg"

    def Initialize(self):
        # Import command modules *here*, so they're always defined when activating
        from Springs.Commands import (
            CreateCompressionSpring,
            CreateExtensionSpring,
            CreateTorsionSpring,
            DisplaySpringInfo,
        )
        from Springs.Preferences.SpringsPreferencePage import SpringsPreferencePage

        # Register commands
        CreateCompressionSpring.register()
        CreateExtensionSpring.register()
        CreateTorsionSpring.register()

        # Build toolbar/menu
        self.list = [
            "Springs_CreateCompressionSpring",
            "Springs_CreateExtensionSpring",
            "Springs_CreateTorsionSpring",
            "Springs_DisplaySpringInfo",
        ]
        self.appendToolbar("Springs", self.list)
        self.appendMenu("Springs", self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(SpringsWorkbench())
