# import json
# import assembly
# from typing import TextIO

from player.base.classes.PObject import PObject, Surface

global windowSurface


def _deep_search(obj: PObject, lt=None):
    if lt is None:
        lt = []
    for child in obj.children:
        _deep_search(child, lt)
        lt.append(child)
    return lt


# 再写下去就要做个编辑器了
# 懒得做，反正物件都会在运行时加载，
# 预制体就不用json加载了，直接写py文件然后import就行了
#
# def create_object_from_file(obj: PObject, file_handle: TextIO):
#     file = file_handle.readlines()
#

# def create_prefab(file_handle: TextIO) -> PObject:
#     global windowSurface
#     prefab_json = json.load(file_handle)
#     n_obj = PObject(prefab_json['name'], windowSurface)
#     # todo read prefab json
#
#     for item in prefab_json['assembly']:
#         if item[0] == ':':
#             assem_type = type(item[::-1][0:-1][::-1])
#             assembly
#             for assem in assembly
#     return n_obj


class PObjectPool(PObject):
    def __init__(self, window_surface: Surface):
        global windowSurface
        windowSurface = window_surface
        super(PObjectPool, self).__init__("root", window_surface)
        # create_object_from_file(self, open(object_file, "r"))

    def start(self):
        for obj in _deep_search(self):
            for assem in obj.assembly:
                assem.onStart()

    def update(self):
        for obj in _deep_search(self):
            for assem in obj.assembly:
                assem.onUpdate()
                # assem.onFixedUpdate()

    def render(self):
        for obj in _deep_search(self):
            for assem in obj.assembly:
                assem.onRender()

    def gui(self):
        for obj in _deep_search(self):
            for assem in obj.assembly:
                assem.onGUI()
