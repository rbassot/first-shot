import pygame
from pygame.locals import *

#custom game class module
import classes

import sys
import os
import random


#----------GAME CONSTANTS----------
#interface
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 600
BLACK = (0, 0, 0)

#player ship
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_HEALTH = 3
FIRING_FRAMES = 4

#enemy ships
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

#lasers
LASER_RANGE = 250
LASER_WIDTH = 3
LASER_HEIGHT = 15

#explosions
EXPLOSION_WIDTH = 75
EXPLOSION_HEIGHT = 75
EXPLOSION_FRAMES = 3

#GAME OVER screen
GAME_OVER_TXT_WIDTH = 500
GAME_OVER_TXT_HEIGHT = 75
RESTART_TXT_WIDTH = 150
RESTART_TXT_HEIGHT = 45
MAIN_MENU_TXT_WIDTH = 175
MAIN_MENU_TXT_HEIGHT = 45

#----------SPRITES----------
#game interface
space_background = 'space_background_colormod.jpg'
healthbar_img = ['healthbar_empty.png', 'healthbar_onelife.png', 'healthbar_twolives.png', 'healthbar_full.png']

#player ship
player_sprites = ['spaceshooter/PNG/playerShip1_green_updatedguns2.png', 'spaceshooter/PNG/playerShip1_green_updatedguns2_fire_effect.png']

#enemies
enemy_sprites = ['spaceshooter/PNG/Enemies/enemyRed1.png', 'spaceshooter/PNG/Enemies/enemyRed2.png', 'spaceshooter/PNG/Enemies/enemyRed3.png',
    'spaceshooter/PNG/Enemies/enemyRed4.png', 'spaceshooter/PNG/Enemies/enemyRed5.png']

#lasers
laser_img = 'spaceshooter/PNG/Lasers/laserGreen06.png'
laser_fire_effect = 'spaceshooter/PNG/Effects/fire11.png'

#explosions
explosion_animation = ['Explosion/explosion1.png', 'Explosion/explosion2.png', 'Explosion/explosion3.png', 'Explosion/explosion4.png', 
    'Explosion/explosion5.png', 'Explosion/explosion6.png', 'Explosion/explosion7.png', 'Explosion/explosion8.png', 'Explosion/explosion9.png', 
    'Explosion/explosion10.png', 'Explosion/explosion11.png']

#GAME OVER screen
game_over_img = 'GAME-OVER.png'
restart_img = 'RESTART.png'
restart_hovered_img = 'RESTART_hovered.png'
main_menu_img = 'MAIN-MENU.png'
main_menu_hovered_img = 'MAIN-MENU_hovered.png'


#----------PYGAME GROUPS----------
#list to hold player instance using pygame's Sprite superclass
player_list = pygame.sprite.Group()

#list to hold all enemy instances
enemy_list = pygame.sprite.Group()

#list to hold all lasers fired (player and enemies)
laser_list = pygame.sprite.Group()

#list to hold all active explosion instances
explosion_list = pygame.sprite.Group()

def main():

    #get absolute file path & initialize OS window placement on screen
    file_path = os.path.dirname(os.path.realpath( __file__ ))
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (175, 25)

    #initialize necessary pygame attributes
    #pygame.init()
    pygame.font.init()
    pygame.display.init()

    #game interface initialization
    game_interface = classes.Interface(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    game_interface.set_background(space_background)
    game_interface.set_caption("Earth Defense")
    game_interface.update_healthbar(healthbar_img[3])

    #game attribute initialization
    #player
    player_ship = classes.PlayerShip(player_list, 425, 400, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_HEALTH)
    player_ship.set_sprite(os.path.join(file_path, player_sprites[0]))

    #a few initial game settings
    clock = pygame.time.Clock()
    interval_start = pygame.time.get_ticks()
    spawn_interval = 5000                      #spawns enemies every 5 seconds, initially
    max_enemies = 5
    enemy_vel = 1

    firing_interval = 250                      #rate of fire of the player ship's lasers
    prev_fire = pygame.time.get_ticks()

    run_program = True
    game_over = False
    final_explosion = True

    
    #------------------------CONTINUOUS GAME LOOP------------------------
    while(run_program):

        #run program at: 1000/60 = ~16 milliseconds per frame (60 FPS)
        pygame.time.delay(16)

        #check stdin & game variables
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run_program = False

        #check for game over
        if game_over and final_explosion:
            game_over_screen(game_interface)
            game_over = False
            final_explosion = True

            #REINIT game interface
            #game_interface = Interface(DISPLAY_WIDTH, DISPLAY_HEIGHT)
            game_interface.set_background(space_background)
            game_interface.update_healthbar(healthbar_img[3])

            #REINIT game attributes
            #player_ship = PlayerShip(425, 400, 50, 50, 3)
            player_ship.set_sprite(player_sprites[0])
            #enemy_list.clear()
            #laser_list.clear()
            #explosion_list.clear()

            #REINIT game settings
            #clock = pygame.time.Clock()
            interval_start = pygame.time.get_ticks()
            spawn_interval = 5000                       #spawns enemies every 5 seconds initially
            max_enemies = 5
            enemy_vel = 1

            firing_interval = 250                      #rate of fire of the player ship's lasers
            prev_fire = pygame.time.get_ticks()



        ##----------PLAYER MAINTENANCE----------
        #get keyboard inputs
        pressed_keys = pygame.key.get_pressed()

        #player ship movement
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            if player_ship.x <= 0 - player_ship.width / 2:
                player_ship.x = (game_interface.display_width - player_ship.width / 2)

            else:
                player_ship.x -= 5

        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            if player_ship.x >= (game_interface.display_width - player_ship.width / 2):
                player_ship.x = 0 - player_ship.width / 2

            else:
                player_ship.x += 5

        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            if player_ship.y <= 0 + player_ship.height / 2:
                pass
            else:
                player_ship.y -= 5

        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            if player_ship.y >= game_interface.display_height - (4 * player_ship.height) / 2:
                pass
            else:
                player_ship.y += 5

        player_ship.update_hitbox()

        
        #player ship sprite maintenance
        if player_ship.get_fire_frame_count() >= FIRING_FRAMES and player_ship.firing:
            player_ship.set_sprite(player_sprites[0])
            player_ship.firing = False

        elif player_ship.firing:
            player_ship.fire_frame_count += 1
    

        #laser firing
        curr_fire = pygame.time.get_ticks()
        if (pressed_keys[pygame.K_RETURN] or pressed_keys[pygame.K_SPACE]) and curr_fire - prev_fire >= firing_interval:

            #x-values to fire from player ship's guns (visual adjustments)
            prev_fire = curr_fire
            new_laser_left = classes.Laser(laser_list, player_ship.x + 4.8, player_ship.y + 15, 3, 15, 5)
            new_laser_left.set_sprite(laser_img)
            new_laser_right = classes.Laser(laser_list, player_ship.x + (player_ship.width - 6), player_ship.y + 15, 3, 15, 5)
            new_laser_right.set_sprite(laser_img)

            #change player ship to firing effect sprite
            player_ship.set_sprite(player_sprites[1])
            player_ship.fire_frame_count = 0
            player_ship.firing = True


        #----------LASER MAINTENANCE----------
        for laser in laser_list:

            hit = False
            
            #check if laser exceeds maximum travel distance
            if laser.get_travel() >= LASER_RANGE:
                laser_list.remove(laser)
                continue

            for enemy in enemy_list:

                #laser collision - eliminates enemy and creates explosion
                if is_collision(laser, enemy):
                    hit = True
                    new_explosion = classes.Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                        explosion_animation, EXPLOSION_FRAMES)
                    enemy_list.remove(enemy)
                    laser_list.remove(laser)
                    break

            if hit == False:
                laser.y -= 1 * laser.vel

            
        #----------ENEMY MAINTENANCE----------
        #spawn in enemies based on elapsed time
        interval_end = pygame.time.get_ticks()
        if interval_end - interval_start >= spawn_interval and len(enemy_list) < max_enemies:

            #reset spawn interval
            interval_start = interval_end

            #spawn enemy
            new_enemy = classes.EnemyShip(enemy_list, random.randint(50, DISPLAY_WIDTH - 50), -50, ENEMY_WIDTH, ENEMY_HEIGHT)
            new_enemy.set_sprite(enemy_sprites[random.randint(0, len(enemy_sprites) - 1)])

        #update enemy positions - enemies move closer to Earth at the set speed
        for enemy in enemy_list:

            #remove enemy and create explosion if it reaches Earth
            if enemy.y >= DISPLAY_HEIGHT - EXPLOSION_HEIGHT / 3:
                new_explosion = classes.Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                    explosion_animation, EXPLOSION_FRAMES)
                enemy_list.remove(enemy)
                
                player_ship.health -= 1

                #check for Game Over
                if player_ship.health == 0:
                    final_explosion = False
                    game_over = True

            else:
                enemy.y += 1 * enemy_vel
                enemy.update_hitbox()


        #update all explosions
        for explosion in explosion_list:

            if explosion.get_frame_count() >= EXPLOSION_FRAMES:

                #eliminate explosion if it has completed the last frame of the animation
                if explosion.index == len(explosion_animation) - 1:
                    explosion_list.remove(explosion)

                    #if it was the game's final explosion, game is now over
                    if final_explosion == False:
                        final_explosion = True

                    continue

                else:
                    explosion.next_sprite()
                    continue

            explosion.frame_count += 1


        #----------FRAME UPDATING----------         

        #update the frame with all modified object attributes
        game_interface.redraw(game_interface.background, 0, 0)

        #if the final explosion was triggered, the explosion animation completes and rest of screen freezes
        if final_explosion:

            player_ship.redraw(game_interface)

            for laser in laser_list:
                laser.redraw(game_interface)

            for enemy in enemy_list:
                enemy.redraw(game_interface)

        for explosion in explosion_list:
            explosion.redraw(game_interface)

        #update Earth healthbar
        game_interface.update_healthbar(healthbar_img[player_ship.health])

        pygame.display.update()


    pygame.quit()



#Function to check is a collision between 2 objects has occurred. Includes multiple cases depending on the objects passed.
def is_collision(object1, object2):

    #PROJECTILE -> OBJECT
    if hasattr(object1, 'hitbox') == False and hasattr(object2, 'hitbox') == True:
    
        #y-values check
        if object1.y < object2.hitbox[1] + object2.hitbox[3] and object1.y + object1.height > object2.hitbox[1]:

            #x-values check
            if object1.x > object2.hitbox[0] and object1.x + object1.width < object2.hitbox[0] + object2.hitbox[2]:
                return True

        return False


    #OBJECT -> OBJECT
    else:
        #y-values check
        if object1.hitbox[1] < object2.hitbox[1] + object2.hitbox[3] and object1.hitbox[1] + object1.hitbox[3] > object2.hitbox[1]:

            #x-values check
            if object1.hitbox[0] > object2.hitbox[0] and object1.hitbox[0] + object1.hitbox[2] < object2.hitbox[0] + object2.hitbox[2]:
                return True

        return False



#MAIN MENU screen controlling
def main_menu_screen(interface):
    pass


#GAME OVER screen controlling
def game_over_screen(interface):

    #draw the GAME OVER screen
    interface.redraw(interface.background, 0, 0)

    game_over_txt = pygame.image.load(game_over_img).convert_alpha()
    game_over_txt = pygame.transform.scale(game_over_txt, (GAME_OVER_TXT_WIDTH, GAME_OVER_TXT_HEIGHT))
    interface.redraw(game_over_txt, (DISPLAY_WIDTH / 2) - (GAME_OVER_TXT_WIDTH / 2), DISPLAY_HEIGHT / 3)

    restart_txt = pygame.image.load(restart_img).convert_alpha()
    restart_txt = pygame.transform.scale(restart_txt, (RESTART_TXT_WIDTH, RESTART_TXT_HEIGHT))
    restart_txt_hovered = pygame.image.load(restart_hovered_img).convert_alpha()
    restart_txt_hovered = pygame.transform.scale(restart_txt_hovered, (RESTART_TXT_WIDTH, RESTART_TXT_HEIGHT))
    interface.redraw(restart_txt, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

    main_menu_txt = pygame.image.load(main_menu_img).convert_alpha()
    main_menu_txt = pygame.transform.scale(main_menu_txt, (MAIN_MENU_TXT_WIDTH, MAIN_MENU_TXT_HEIGHT))
    main_menu_txt_hovered = pygame.image.load(main_menu_hovered_img).convert_alpha()
    main_menu_txt_hovered = pygame.transform.scale(main_menu_txt_hovered, (MAIN_MENU_TXT_WIDTH, MAIN_MENU_TXT_HEIGHT))
    interface.redraw(main_menu_txt, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

    pygame.display.update()


    #wait for user input loop
    input_wait = True
    mouse_click = False

    restart_button = False
    main_menu_button = False


    while input_wait:

        #get cursor's location
        cursor = pygame.mouse.get_pos()
        cursor_x = cursor[0]
        cursor_y = cursor[1]

        restart_button = False
        main_menu_button = False

        #check RESTART button
        if (cursor_x > (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2) and cursor_x < (DISPLAY_WIDTH / 2) + (RESTART_TXT_WIDTH / 2) and
                cursor_y > (DISPLAY_HEIGHT * (5/9)) and cursor_y < (DISPLAY_HEIGHT * (5/9)) + (RESTART_TXT_HEIGHT)):
                
            restart_button = True

        #check MAIN MENU button
        elif (cursor_x > (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2) and cursor_x < (DISPLAY_WIDTH / 2) + (MAIN_MENU_TXT_WIDTH / 2) and
                cursor_y > (DISPLAY_HEIGHT * (4/6)) and cursor_y < (DISPLAY_HEIGHT * (4/6)) + (MAIN_MENU_TXT_HEIGHT)):

            main_menu_button = True


        #update text upon mouse hover
        #RESTART button
        if restart_button:
            interface.redraw(restart_txt_hovered, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

        else:
            interface.redraw(restart_txt, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

        #MAIN MENU button
        if main_menu_button:
            interface.redraw(main_menu_txt_hovered, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

        else:
            interface.redraw(main_menu_txt, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

        pygame.display.update()


        #check for mouse click
        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True

            #check for user option selection
            if mouse_click and event.type == MOUSEBUTTONUP and restart_button:
                input_wait = False

            elif mouse_click and event.type == MOUSEBUTTONUP and main_menu_button:
                input_wait = False

    return




if __name__ == '__main__':
    main()