from FGAme import *
from sfx import SFX
from enemy import *
import os
import pygame
from pygame.locals import *
_ROOT = os.path.abspath(os.path.dirname(__file__))

PLAYERCHARGES = USEREVENT + 2

class Player(AABB):
    def __init__(self, armor_health, shot_charges, special_charges, turbo_charges, shield_charges, *args, **kwargs):
        self.armor_health = armor_health
        self.shot_charges = shot_charges
        self.special_charges = special_charges
        self.turbo_charges = turbo_charges
        self.shield_charges = shield_charges
        super(Player, self).__init__(*args, **kwargs)
        self.create_charges(self)
        # on('pre-collision').do(sound_hit)

    def move_player(self, dx, dy):
        self.vel += (dx, dy)

    def shield(self, player_mass, player_color, shield_charges):
        if self.shield_charges > 0:
            # shield_sfx = os.path.join(_ROOT, 'sfx/shield.wav')
            # Music.play_sound(shield_sfx)
            self.vel = vec(0, 0)
            self.mass *= 10
            self.color = 'darkblue'
            schedule(1, self.shield_cooldown, player_mass=player_mass, player_color=player_color, shield_charges=shield_charges)
        else:
            pass

    def shield_cooldown(self, player_mass, player_color, shield_charges):
        self.mass = player_mass
        self.color = player_color
        self.shield_charges -= 1

    def special_move(self, world, special_charges):
        if special_charges > 0:
            shot = RegularPoly(10,
                length=15,
                pos=(self.pos.x, self.pos.y + 40),
                vel=(0,550),
                omega=20,
                color='blue',
                mass='inf')
            world.add(shot)
            self.special_charges -= 1
        else:
            pass

    def shot(self, world, shot_charges):
        if shot_charges > 0:
            shot_sound = os.path.join(_ROOT, 'sfx/shot.wav')
            SFX.play_sound(shot_sound)
            shot = AABB(
                shape=(2, 3),
                pos=(self.pos.x, self.pos.y+20),
                vel=(0, 1000),
                mass='inf',
                color='blue')
            world.add(shot)
            self.shot_charges -= 1
        else:
            pass

    def turbo(self, turbo_charges):
        if turbo_charges > 0:
            self.vel *= 3
            self.turbo_charges -= 1
        else:
            pass

    def create_charges(self, *args, **kwargs):
        PLAYERCHARGES = USEREVENT + 2
        pygame.time.set_timer(PLAYERCHARGES, 3500)

    def charges_listener(self, shot_charges, turbo_charges, shield_charges, special_charges):
        if pygame.event.get(PLAYERCHARGES): 
            self.refill_charges(shot_charges, turbo_charges, shield_charges, special_charges)

    def refill_charges(self, shot_charges, turbo_charges, shield_charges, special_charges):
        if special_charges == 0 and shot_charges == 0:
            self.special_charges = 1
        if shot_charges == 0:
            self.shot_charges = 10
        if turbo_charges < 3:
            self.turbo_charges += 1
        if shield_charges == 0:
            self.shield_charges = 1
        else:
            pass


    # def sound_hit(self, col, dx):
    #     sound_hit = os.path.join(_ROOT, 'sfx/hit.wav')
    #     SFX.play_sound(sound_hit)

    def check_defeat(self):
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            print("DERROTA. Você foi destruido.")
            exit()
        elif self.armor_health <= 0:
            print("DERROTA. Você foi destruido.")
            exit()

    @listen('post-collision')
    def detect_hit(arena, col):
        A, B = col
        if isinstance(A, Player) and isinstance(B, Enemy):
            multi_damage = 0
            while(multi_damage < 3):
                A.deal_damage()
            B.deal_damage()
        elif isinstance(A, Enemy) and isinstance(B, Player):
            multi_damage = 0
            while(multi_damage < 3):
                B.deal_damage()
            A.deal_damage()
        elif isinstance(A, Player) and isinstance(B, Circle):
            multi_damage = 0
            while(multi_damage < 2):
                A.deal_damage()
        elif isinstance(A, Circle) and isinstance(B, Player):
            multi_damage = 0
            while(multi_damage < 2):
                B.deal_damage()
        elif isinstance(A, AABB) and isinstance(B, Player):
            B.deal_damage()
        elif isinstance(A, Player) and isinstance(B, AABB):
            A.deal_damage()
            
    def deal_damage(self):
        self.armor_health -= 10
