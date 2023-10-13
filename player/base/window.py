import pygame.display

from classes.PObjectPool import PObjectPool

global object_pool  # , prefab_object_file


# prefab_object_file = "./pre.json"


def init():
    global object_pool  # , prefab_object_file
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((2560, 600))
    object_pool = PObjectPool(screen)
    object_pool.start()
    while True:
        object_pool.update()
        object_pool.render()
        object_pool.gui()


init()
