from pygame.surface import Surface


class PObject:
    name: str = ""
    layer: int = 0
    assembly: list = []
    children: list = []
    isEnabled: bool = True
    surface: Surface = None
    windowSurface: Surface = None

    def __init__(self, name: str, window_surface: Surface):
        self.name = name
        self.windowSurface = window_surface

    def getAssembly(self, assem_type: type):
        for assem in self.assembly:
            if type(assem) is assem_type:
                return assem
