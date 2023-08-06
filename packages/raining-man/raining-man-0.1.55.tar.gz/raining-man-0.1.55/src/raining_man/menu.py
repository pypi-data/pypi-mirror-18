import pygame
from pygame.locals import *
from sys import exit
from .core import Media

class Menu():
    def __init__(self):
        self.next = self
        self.index = 0
        self.screen = pygame.display.set_mode((800,600), 0, 32)
        self.caption = pygame.display.set_caption("Main Menu")
        self.start_action = False

    def get_key_input(self):
        for event in pygame.event.get():
            start_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self.index == 0:
                    self.index += 1
                elif event.key == pygame.K_UP and self.index == 1:
                    self.index -= 1

                if (self.index == 0) and event.key == pygame.K_RETURN:
                    start_game = True
                elif (self.index == 1) and event.key == pygame.K_RETURN:
                    exit()

            if event.type == QUIT:
                    exit()

            return start_game

    def set_buttons(self):
        start_button = Media.change_image('images/jogar.png').convert_alpha()
        exit_button = Media.change_image('images/sair.png').convert_alpha()

        if(self.index == 0):
            start_button = Media.change_image('images/jogar_selecionado.png').convert_alpha()
        else:
            exit_button = Media.change_image('images/sair_selecionado.png').convert_alpha()

        self.screen.blit(start_button,(300,400),start_button.get_rect())
        self.screen.blit(exit_button,(320,500),exit_button.get_rect())

    def render(self):
        bg = Media.change_image('images/menu.png').convert_alpha()
        clock = pygame.time.Clock()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        Media.change_music("sounds/menu_music.mp3")

        while True:
            self.screen.blit(bg, (0, 0), bg.get_rect())
            self.set_buttons()
            offset_height = 50# Sets the space between lines at main menu scene.
            i = 0

            option = self.get_key_input()

            if(option): # Quit main menu loop
                break

            pygame.display.update()
            time_passed = clock.tick(30)

