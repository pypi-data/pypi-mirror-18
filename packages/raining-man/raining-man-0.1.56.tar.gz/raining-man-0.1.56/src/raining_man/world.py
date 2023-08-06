from FGAme import *
from .boy import Boy
from .shot import Shot
from .core import randomize, Media, Physics, Timer
from pygame.locals import *
from .menu import *
import pygame
import time
import shelve

def new_game():
    """
        Creates the objects needed to run the game.
    """
    # Menu objects
    main_menu = Menu()
    main_menu.render() # PLayer will be stuck here until enter an option
    # Start the game objects
    world = RainingWorld()
    world = RainingWorld()
    world.add_raining_world()
    world.start_sound()
    world.render_game()

class RainingWorld(World):

    def __init__(self):
        super().__init__()
        self.base_k = 1.05
        self.recover_interval = 150
        self.time_to_exaust = 200
        self.spawn_time = 130
        self.screen_end = -10
        self.gravity = (0, 30)
        self.shot_list = []
        self.count = 0
        self.points = 0
        self.is_exaust = False
        self.timer = 0 # GAME TIMER
        self.exaustion_timer = 0
        self.recover_timer = 0
        self.vel = (0, 100)
        self.best_score = Media.get_score()

    def finish_game(self, screen):
        Media.change_music('sounds/battle_theme.mp3')
        time.sleep(1)

        if self.points > self.best_score:
            self.best_score = self.points
        Media.save_score(self.best_score)

        new_game()

    def add_raining_world(self):
        """
        :returns: nothing

        create the objects to the rainging world

        """

        self.add.margin(200, -500)
        self.gravity = (0, -10)

        self.player = Boy()
        self.player.gravity = (0, 0)
        self.add(self.player)
        shot = Shot() # INITIAL SHOT
        self.shot_list.append(shot)

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

    def start_sound(self):
        """
        Play initial sound to the game

        """
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        Media.change_music("sounds/sound-adventure.mp3")

    def render_game(self):
        pygame.font.init()
        background = Media.change_image('images/background.png')
        text = Media.define_text()
        screen = pygame.display.set_mode((800, 600), 0, 32)
        best_score = "%05d" % (self.best_score)
        Media.start_text(screen, best_score)
        self.caption = pygame.display.set_caption("Raining Man")
        clock = pygame.time.Clock()
        while True:
            screen.blit(background, (200, 0))
            diff = (self.player.width / 2, self.player.height / 2)
            new_pos = self.player.pos - diff
            screen.blit(self.player.body_pygame.convert_alpha(), 
                                    new_pos, self.player.rectangle)

            self.update(screen, text)

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_RIGHT]:
                    if self.player.pos[0] <= 588:
                            self.player.move_p1(2)
            elif pressed_keys[K_LEFT]:
                    if self.player.pos[0] >= 215:
                            self.player.move_p1(-2)

            if pressed_keys[K_UP]:
                Physics.increase_drag(self)
            elif not pressed_keys[K_UP] or self.is_exaust:
                self.player.body_pygame = Media.change_image('images/1.png')
                Physics.decrease_drag(self)

            pygame.display.update()
            time_passed = clock.tick(60)

    
    def update(self, screen, text):
        if self.timer >= self.spawn_time:
            self.timer = 0
            self.vel = (0, self.vel[1] + self.count)
            randomize(self.shot_list, self.count, self.vel)

        for shot in self.shot_list:
            shot.gravity = self.gravity
            shot.vel = self.shot_list[0].vel
            new_pos = shot.pos - (shot.width / 2, shot.height / 2)
            screen.blit(shot.body_pygame.convert_alpha(), 
                                    new_pos)
            shot.update()

            if shot.pos[1] < self.screen_end:
                self.shot_list.remove(shot)
                self.count = self.count + 2
                self.points = self.points + 10 + self.count
                string_points = "%05d" % (self.points)
                string_best = "%05d" % (self.best_score)
                Media.update_text(string_points, screen, text, string_best)

        if Physics.see_colision(self.shot_list, self.player):
            game_over = Media.change_image("images/gameover.png")
            screen.blit(game_over.convert_alpha(), (300, 300), \
                        game_over.get_rect())
            self.finish_game(screen)

        Timer.count(self)
