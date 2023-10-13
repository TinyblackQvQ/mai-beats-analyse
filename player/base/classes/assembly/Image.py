from pygame import image, transform
from pygame.surface import Surface

import AssemblyBase
import Transform


class Image(AssemblyBase):
    surface: Surface = None
    file_path: str = ""

    def __init__(self, img_file):
        self.file_path = img_file
        self.loadImg()

    def loadImg(self, img_file: str = None):
        if img_file is not None:
            self.file_path = img_file
        self.surface = image.load(self.file_path)

    def onRender(self):
        assem_transform = self.Object.getAssembly(Transform)
        img_size = self.surface.get_size()
        n_sur = transform.scale(self.surface, (assem_transform.scale.toTuple()))
        n_sur = transform.rotate(n_sur, assem_transform.rotation)
        pos = assem_transform.position.x - img_size[0] / 2, assem_transform.position.x - img_size[1] / 2
        Surface.blit(self.Object.windowSurface, n_sur, pos)
