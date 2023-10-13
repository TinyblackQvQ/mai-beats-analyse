from IAssembly import IAssembly

from player.base.classes.PObject import PObject


class AssemblyBase(IAssembly):
    name: str = ""
    Object: PObject = None
    isEnabled: bool = True

    def __init__(self, attached: PObject):
        self.attached = attached
        self.onCreate()

    def __del__(self):
        self.onDestroy()

    def enable(self):
        self.onEnable()

    def disable(self):
        self.onDisable()

    def onCreate(self):
        pass

    def onEnable(self):
        pass

    def onStart(self):
        pass

    def onUpdate(self):
        pass

    def onFixedUpdate(self):
        pass

    def onRender(self):
        pass

    def onGUI(self):
        pass

    def onDisable(self):
        pass

    def onDestroy(self):
        pass
