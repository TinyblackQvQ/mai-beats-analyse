from abc import abstractmethod

class IAssembly:
    @abstractmethod
    def onCreate(self): ...

    @abstractmethod
    def onEnable(self): ...

    @abstractmethod
    def onStart(self): ...

    @abstractmethod
    def onUpdate(self): ...

    @abstractmethod
    def onFixedUpdate(self): ...

    @abstractmethod
    def onRender(self): ...

    @abstractmethod
    def onGUI(self): ...

    @abstractmethod
    def onDisable(self): ...

    @abstractmethod
    def onDestroy(self): ...
