try:
    import FreeCADGui
except ImportError:
    FreeCADGui = None

class ViewProviderSpring:
    def __init__(self, vobj):
        if FreeCADGui is None or vobj is None:
            return
        vobj.Proxy = self

    def attach(self, vobj):
        pass

    def updateData(self, fp, prop):
        pass

    def getDisplayModes(self, obj):
        return ["Shaded"]

    def getDefaultDisplayMode(self):
        return "Shaded"

    def setDisplayMode(self, mode):
        return mode

    def onChanged(self, vobj, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
