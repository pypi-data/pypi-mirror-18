from .world import new_game
import pygame
from pygame.locals import *
from raining_man.shot import Shot
import random
import time
import os
from .menu import *


def start():
    new_game()
