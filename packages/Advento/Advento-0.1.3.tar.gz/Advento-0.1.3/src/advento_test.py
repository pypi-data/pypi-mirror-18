# Importacao de pacotes
from FGAme import *
import pygame
from pygame.locals import *

# Contadores e marcadores globais
shot_charges = 10
special_charges = 1
turbo_charges = 3
shield_charges = 1

# Mundo
world = World()
world.damping=2

# Personagem
char1 = AABB(shape=(15, 25), pos=(400, 35), color='blue', mass=150)
char1.inertia /= 2
char1.restitution = 0

# Inimigo
enemy1 = AABB(shape=(35, 35), pos=(400, 530), color='red', mass='inf', vel=(300,0), restitution=0)
enemy1.inertia = 'inf'

# Plataformas
platform1 = world.add.aabb(shape=(115, 10), pos=(67, 452), mass='inf')
platform2 = world.add.aabb(shape=(87, 10), pos=(235, 150), mass='inf')
platform3 = world.add.aabb(shape=(122, 10), pos=(400, 350), mass='inf')
platform4 = world.add.aabb(shape=(115, 10), pos=(650, 75), mass='inf')
platform5 = world.add.aabb(shape=(53, 10), pos=(625, 250), mass='inf')
platform6 = world.add.aabb(shape=(67, 10), pos=(750, 440), mass='inf')

# Comando de movimentacao para a direita
@listen('long-press', 'right')
def move_right():
    char1.vel = (char1.vel.x+25, char1.vel.y)

# Comando de movimentacao para a esquerda
@listen('long-press', 'left')
def move_left():
    char1.vel = (char1.vel.x-25, char1.vel.y)

# Comando de movimentacao para frente
@listen('long-press', 'up')
def move_left():
    char1.vel = (char1.vel.x, char1.vel.y+25)

# Comando de movimentacao para trás
@listen('long-press', 'down')
def move_left():
    char1.vel = (char1.vel.x, char1.vel.y-25)

# Comando de turbo
@listen('key-down', 'w')
def turbo():
    if turbo_charges > 0:
        char1.vel = char1.vel*3
        global turbo_charges
        turbo_charges -= 1
    else:
        pass


# Comando de tiro do jogador
@listen('key-down', 'q')
def player_shot():
    if shot_charges > 0:
        shot = world.add.aabb(
            shape=(2, 3),
            pos=(char1.pos.x, char1.pos.y+20),
            vel=(0, 1000),
            mass='inf',
            color='blue')
        global shot_charges
        shot_charges -= 1
    else:
        pass


# Comando de escudo do jogador
@listen('key-down','e')
def player_shield():
    if shield_charges > 0:
        char1.vel/=10
        char1.mass *= 10
        char1.color='darkblue'
        global shield_charges
        shield_charges -= 1
        schedule(1,shield_cooldown)
    else:
        pass

def shield_cooldown():
    char1.mass /= 10
    char1.color='blue'


# Comando de especial
@listen('key-down', 'r')
def special_move():
    if special_charges > 0:
        shot = RegularPoly(10,
            length=30,
            pos=(char1.pos.x, char1.pos.y + 40),
            vel=(0,550),
            omega=20,
            color='blue',
            mass='inf')
        world.add(shot)
        global special_charges
        special_charges -= 1
    else:
        pass


# Movimentacao do inimigo
@listen('frame-enter')
def enemy_movement():
    if enemy1.x >= 750:
        enemy1.vel = (enemy1.vel.x*(-1), enemy1.vel.y)
    elif enemy1.x <= 50:
        enemy1.vel = (enemy1.vel.x*(-1), enemy1.vel.y)


# Tiro do inimigo
ENEMYSHOT = USEREVENT + 1
pygame.time.set_timer(ENEMYSHOT, 500)

@listen('frame-enter')
def shot_listener():
    if pygame.event.get(ENEMYSHOT): 
        enemy_shot()

def enemy_shot():
    shot = Circle(3,
        pos=(enemy1.pos.x, enemy1.pos.y-40),
        vel=(0, -500),
        mass='inf',
        color='red')
    world.add(shot)


# Recarregar habilidades
PLAYERCHARGES = USEREVENT + 2
pygame.time.set_timer(PLAYERCHARGES, 3500)

@listen('frame-enter')
def charges_listener():
    if pygame.event.get(PLAYERCHARGES): 
        refill_charges()

def refill_charges():
    if special_charges == 0 and shot_charges == 0:
        global special_charges
        special_charges = 1
    if shot_charges == 0:
        global shot_charges
        shot_charges = 10
    if turbo_charges < 3:
        global turbo_charges
        turbo_charges += 1
    if shield_charges == 0:
        global shield_charges
        shield_charges = 1
    else:
        pass
        


# Eliminar tiros fora de cena
@listen('frame-enter')
def remove_outbound_shot():
    try:
        if shot.pos.x<0 or shot.pos.x>600:
            world.remove(shot)
        elif shot.pos.y<0 or shot.pos.y>800:
            world.remove(shot)
        else:
            pass
    except NameError:
        pass
    else:
        pass


# Condicao de fim de jogo
@listen('frame-enter')
def check_player_lose():
    if char1.x < -10 or char1.x > 810 or char1.y < -10 or char1.y > 610:
        world.pause()


# Adiciona elementos ao mundo
world.add(char1)
world.add(enemy1)
world.add.margin(10,0,10,0)

run()
