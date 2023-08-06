import random
import os
import pygame
from FGAme import *
from pygame.locals import *

class Physics(object):

    """Docstring for Physics.
    This class do activicts to world physics.
    """

    def drag(shot):
        x, y = shot.vel
        drag = abs(shot.k * (y ** 2))
        a = (shot.mass * shot.gravity[1] - drag) / shot.mass
        speed_x, speed_y = shot.vel
        speed_y += a * 1/60
        pos_x, pos_y = shot.pos
        pos_y -= speed_y * 1/60

        return (speed_x, speed_y), (pos_x, pos_y)

    def increase_drag(world):
        if not world.is_exaust:
            world.player.body_pygame = Media.change_image('images/2.png')
            for shot in world.shot_list:
                shot.k = 100
        else:
            world.player.body_pygame = Media.change_image('images/1.png')

    def decrease_drag(world):
        for shot in world.shot_list:
            shot.k = world.base_k

    @staticmethod
    def get_surface_rectangle(game_object):
        width = game_object.body_pygame.get_width()	
        height = game_object.body_pygame.get_height()

        new_pos = game_object.pos - (game_object.width / 2, game_object.height / 2)

        rect = Rect(new_pos[0], new_pos[1], width - 20, height)

        return rect

    @staticmethod
    def colision(shot, player):
        shot_rect = Physics.get_surface_rectangle(shot)
        player_rect = Physics.get_surface_rectangle(player)

        if player_rect.colliderect(shot_rect):
                return True

        return False

    @staticmethod
    def see_colision(shot_list, player):
        return_method = False
        for shot in shot_list:
            if Physics.colision(shot, player):
                return_method = True
        return return_method

def randomize(shot_list, count, world_vel):
    for i in range(random.randint(1, 3)):
        from .shot import Shot
        shot = Shot()
        count = count + 1
        randomizer = random.randint(30, 70)
        shot.x = 220 + (randomizer + (110 * (i)))
        shot.y = shot.y + random.randint(-80, -50) # TO NOT GET TOGETHER
        shot_list.append(shot)
        shot.vel = world_vel

class Media():
    @staticmethod
    def change_image(img):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, img)
        return pygame.image.load(absolute_image_path)

    @staticmethod
    def change_music(music):
        _ROOT = os.path.abspath(os.path.dirname(__file__))
        absolute_image_path = os.path.join(_ROOT, music)
        dash_sound =  pygame.mixer.music.load(absolute_image_path)
        dash_sound = pygame.mixer.music.play()

    @staticmethod
    def update_text(string_points, screen, text):
        point_label = text.get('point').render(
                string_points,
                1,
                text.get('black'))

        screen.fill(text.get('white'))

        # render text
        screen.blit(text.get('tittle'), (10, 50))
        screen.blit(point_label, (10, 80))

    @staticmethod
    def define_text():
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        title_font = pygame.font.SysFont("monospace", 25)
        title_label = title_font.render("Raining Man", 1, BLACK)
        point_font = pygame.font.SysFont("monospace", 15)

        text = {
                'white': WHITE,
                'black': BLACK,
                'tittle': title_label,
                'point': point_font,
                }
        return text

    @staticmethod
    def start_text(screen):
        # initialize font;
        title_font = pygame.font.SysFont("monospace", 25)
        point_font = pygame.font.SysFont("monospace", 15)
        
        #define colors
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        #define text
        title_label = title_font.render("Raining Man", 1, BLACK)
        point_label = point_font.render("00000", 1, BLACK)

        screen.fill(WHITE)

        # render text
        screen.blit(title_label, (10, 50))
        screen.blit(point_label, (10, 80))

class Timer(object):

    """Docstring for Timer.
    Class to manipule the time to make colosions and
    count the time to exaust
    """
    @staticmethod
    def count(world):
        # TIMER INCREASING DEPENDS ON K VALUE
        if not world.shot_list:
            world.timer += 1
        elif (world.shot_list[0].k) == world.base_k:
            world.timer += 1
            if world.exaustion_timer >= world.time_to_exaust:
                world.recover_timer += 1
                if world.recover_timer > world.recover_interval:
                    world.exaustion_timer = 0
                    world.is_exaust = False
                    world.recover_timer = 0
        else: # SLOW DOWN THE TIME
            world.timer += 0.5
            if world.exaustion_timer >= world.time_to_exaust:
                for shot in world.shot_list:
                    shot.k = world.base_k
                world.is_exaust = True
            else:
                world.exaustion_timer += 1
