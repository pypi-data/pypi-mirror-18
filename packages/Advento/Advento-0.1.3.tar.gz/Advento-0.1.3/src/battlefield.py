from FGAme import *
from player import Player
from enemy import Enemy
from sfx import SFX
import os
import pygame
from pygame.locals import *
_ROOT = os.path.abspath(os.path.dirname(__file__))


class Battlefield(World):
    def init(self):
        self.player = Player(shape=(15, 25),
                            pos=(400, 35),
                            color='blue',
                            mass=150,
                            armor_health=100,
                            shot_charges = 10,
                            special_charges = 1,
                            turbo_charges = 3,
                            shield_charges = 1)
        self.enemy = Enemy(shape=(35, 35),
                            pos=(400, 530),
                            color='red',
                            mass='inf',
                            vel=(300,0),
                            armor_health=100)
        self.add([self.player, self.enemy])
        self.damping = 2

        # main_theme = os.path.join(_ROOT, 'sfx/main_theme.mp3')
        # SFX.play_music(main_theme)

        self.draw_platforms()
        self.draw_margin()

        on('long-press', 'left').do(self.player.move_player, -25, 0)
        on('long-press', 'right').do(self.player.move_player, 25, 0)
        on('long-press', 'up').do(self.player.move_player, 0, 25)
        on('long-press', 'down').do(self.player.move_player, 0, -25)
        on('key-down', 'q').do(self.player.shot, self, self.player.special_charges)
        on('key-down', 'w').do(self.player.turbo, self.player.turbo_charges)
        on('key-down', 'e').do(self.player.shield, self.player.mass, self.player.color, self.player.shield_charges)
        on('key-down', 'r').do(self.player.special_move, self, self.player.special_charges)
        on('frame-enter').do(self.player.charges_listener,
                            self.player.shot_charges,
                            self.player.turbo_charges,
                            self.player.shield_charges,
                            self.player.special_charges)
        on('frame-enter').do(self.enemy.enemy_shot_listener, self)
        on('frame-enter').do(self.enemy.enemy_movement, self.enemy.vel)
        on('frame-enter').do(self.remove_out_of_bounds_shot)
        on('frame-enter').do(self.player.check_defeat)
        on('frame-enter').do(self.enemy.check_defeat)

    def draw_platforms(self):
        self.platform1 = self.add.aabb(shape=(115, 10), pos=(67, 452), mass='inf')
        self.platform2 = self.add.aabb(shape=(87, 15), pos=(235, 150), mass='inf')
        self.platform3 = self.add.aabb(shape=(122, 10), pos=(400, 350), mass='inf')
        self.platform4 = self.add.aabb(shape=(115, 20), pos=(650, 75), mass='inf')
        self.platform5 = self.add.aabb(shape=(53, 15), pos=(625, 250), mass='inf')
        self.platform6 = self.add.aabb(shape=(67, 10), pos=(750, 440), mass='inf')

    def remove_out_of_bounds_shot(self):
        try:
            if shot.pos.x<0 or shot.pos.x>600:
                self.remove(shot)
            elif shot.pos.y<0 or shot.pos.y>800:
                self.remove(shot)
            else:
                pass
        except NameError:
            pass
        else:
            pass

    def draw_margin(self):
        self.add.margin(10,0,10,0)
