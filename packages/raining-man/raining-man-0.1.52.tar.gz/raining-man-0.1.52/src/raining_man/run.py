from .world import RainingWorld
import pygame
from pygame.locals import *
from raining_man.shot import Shot
import random
import time
import os
from .menu import *


def start():
	# Menu objects
	main_menu = Menu()
	main_menu.render() # PLayer will be stuck here until enter an option

	# Start the game objects
	world = RainingWorld()
	world.add_raining_world()
	world.start_sound()
	world.render_game()
