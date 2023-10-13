from player.base.classes.assembly.AssemblyBase import AssemblyBase
from player.base.classes.base.Vector import Vector


class Transform(AssemblyBase):
    position: Vector = Vector(0, 0)
    rotation: float = 0
    scale: Vector = Vector(0, 0)
