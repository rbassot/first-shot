import pygame
from pygame.locals import *

#custom game class module
from classes import *

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
FIRING_FRAMES = 9
STUN_BLIT_RATE = 30
STUN_FRAME_DURATION = 240
PLAYER_POWERUP_DURATION = 15

#enemy ships
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

#lasers
LASER_RANGE = 250
LASER_WIDTH = 3
LASER_HEIGHT = 15
LASER_VEL = 5

#explosions
EXPLOSION_WIDTH = 75
EXPLOSION_HEIGHT = 75
EXPLOSION_FRAMES = 3

#powerups
POWERUP_WIDTH = 25
POWERUP_HEIGHT = 25
POWERUP_DURATION_SEC = 10
POWERUP_FLASHING_SEC = 6
POWERUP_FLASH_RATE = 45
POWERUP_FRAME_DURATION = 800
POWERUP_FLASHING_FRAMES = 300

#MAIN MENU screen
TITLE_TXT_WIDTH = 600
TITLE_TXT_HEIGHT = 75
START_TXT_WIDTH = 325
START_TXT_HEIGHT = 45
CREDITS_TXT_WIDTH = 135
CREDITS_TXT_HEIGHT = 35

#GAME OVER screen
GAME_OVER_TXT_WIDTH = 500
GAME_OVER_TXT_HEIGHT = 75
RESTART_TXT_WIDTH = 150
RESTART_TXT_HEIGHT = 45
MAIN_MENU_TXT_WIDTH = 175
MAIN_MENU_TXT_HEIGHT = 45

#----------SPRITES----------
#game interface
space_background = 'images/backgrounds/space_background_colormod.jpg'
main_menu_background = 'images/backgrounds/black.png'
healthbar_imgs = ['images/UI/healthbar_empty.png',
                 'images/UI/healthbar_onelife.png', 
                 'images/UI/healthbar_twolives.png', 
                 'images/UI/healthbar_full.png']

#player ship
player_sprites = ['images/sprites/playerShip1_green_updatedguns2.png',
                'images/sprites/playerShip1_green_updatedguns2_fire_effect.png']

#enemies
enemy_sprites = ['images/sprites/enemyRed1.png',
                'images/sprites/enemyRed2.png',
                'images/sprites/enemyRed3.png',
                'images/sprites/enemyRed4.png',
                'images/sprites/enemyRed5.png']

#lasers
laser_img = 'images/sprites/laserGreen06.png'

#explosions
explosion_animation = ['images/sprites/explosion/explosion1.png',
                    'images/sprites/explosion/explosion2.png',
                    'images/sprites/explosion/explosion3.png',
                    'images/sprites/explosion/explosion4.png',
                    'images/sprites/explosion/explosion5.png',
                    'images/sprites/explosion/explosion6.png',
                    'images/sprites/explosion/explosion7.png',
                    'images/sprites/explosion/explosion8.png',
                    'images/sprites/explosion/explosion9.png', 
                    'images/sprites/explosion/explosion10.png',
                    'images/sprites/explosion/explosion11.png']

#powerups
powerup_imgs = {}
powerup_imgs['bubble_shield'] = 'images/sprites/powerups/shield_green_custom.png'
powerup_imgs['fire_rate'] = 'images/sprites/powerups/ammo_blue_custom.png'
powerup_imgs['health_up'] = 'images/sprites/powerups/pill_red.png'
powerup_imgs['zap_field'] = 'images/sprites/powerups/bolt_gold.png'

#MAIN MENU screen
title_txt_img = 'images/menus/EARTH-DEFENSE.png'
start_txt_img = 'images/menus/CLICK-HERE-TO-PLAY.png'
start_txt_hovered_img = 'images/menus/CLICK-HERE-TO-PLAY-HOVERED.png'
credits_txt_img = 'images/menus/CREDITS.png'
credits_txt_hovered_img = 'images/menus/CREDITS-HOVERED.png'

#GAME OVER screen
game_over_img = 'images/menus/GAME-OVER.png'
restart_img = 'images/menus/RESTART.png'
restart_hovered_img = 'images/menus/RESTART_hovered.png'
main_menu_img = 'images/menus/MAIN-MENU.png'
main_menu_hovered_img = 'images/menus/MAIN-MENU_hovered.png'

#----------MUSIC & SOUND FX----------
#main game music
game_music = "music/Eric Skiff - We're all under the stars.mp3"

#player laser firing
player_firing_sound = 'soundfx/270343__littlerobotsoundfactory__shoot-01.wav'

#explosion effect
'''TO IMPLEMENT'''


#----------GAME MAINTENANCE----------
class Main(object):

    '''Main object initialization'''
    def __init__(self, interface):

        #initialize OS window placement on screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (175, 25)

        #game interface setup
        self.interface = interface
        self.interface.set_background(main_menu_background)
        self.exit = False

        #game music & caption initialization
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)
        self.interface.set_caption("Earth Defense")


    '''Main Menu screen maintenance'''
    def main_menu_screen(self):

        #draw MAIN MENU screen
        self.interface.redraw(self.interface.background, 0, 0)

        title_txt = pygame.image.load(title_txt_img).convert_alpha()
        title_txt = pygame.transform.scale(title_txt, (TITLE_TXT_WIDTH, TITLE_TXT_HEIGHT))
        self.interface.redraw(title_txt, (DISPLAY_WIDTH / 2) - (TITLE_TXT_WIDTH / 2), DISPLAY_HEIGHT / 8)

        start_txt = pygame.image.load(start_txt_img).convert_alpha()
        start_txt = pygame.transform.scale(start_txt, (START_TXT_WIDTH, START_TXT_HEIGHT))
        start_txt_hovered = pygame.image.load(start_txt_hovered_img).convert_alpha()
        start_txt_hovered = pygame.transform.scale(start_txt_hovered, (START_TXT_WIDTH, START_TXT_HEIGHT))
        self.interface.redraw(start_txt, (DISPLAY_WIDTH / 2) - (START_TXT_WIDTH / 2), DISPLAY_HEIGHT * (9/12))

        credits_txt = pygame.image.load(credits_txt_img).convert_alpha()
        credits_txt = pygame.transform.scale(credits_txt, (CREDITS_TXT_WIDTH, CREDITS_TXT_HEIGHT))
        credits_txt_hovered = pygame.image.load(credits_txt_hovered_img).convert_alpha()
        credits_txt_hovered = pygame.transform.scale(credits_txt_hovered, (CREDITS_TXT_WIDTH, CREDITS_TXT_HEIGHT))
        self.interface.redraw(credits_txt, (DISPLAY_WIDTH / 2) - (CREDITS_TXT_WIDTH / 2), DISPLAY_HEIGHT * (12/14))

        self.interface.update()

        #wait for user input
        input_wait = True
        mouse_click = False
        start_button = False
        credits_button = False

        while input_wait:

            #get cursor's location
            cursor = pygame.mouse.get_pos()
            cursor_x = cursor[0]
            cursor_y = cursor[1]

            start_button = False
            credits_button = False

            #Check button hover states
            #START button
            if (cursor_x > (DISPLAY_WIDTH / 2) - (START_TXT_WIDTH / 2) and cursor_x < (DISPLAY_WIDTH / 2) + (START_TXT_WIDTH / 2) and
                    cursor_y > (DISPLAY_HEIGHT * (9/12)) and cursor_y < (DISPLAY_HEIGHT * (9/12)) + (START_TXT_HEIGHT)):
                    
                start_button = True

            #CREDITS button
            elif (cursor_x > (DISPLAY_WIDTH / 2) - (CREDITS_TXT_WIDTH / 2) and cursor_x < (DISPLAY_WIDTH / 2) + (CREDITS_TXT_WIDTH / 2) and
                    cursor_y > (DISPLAY_HEIGHT * (12/14)) and cursor_y < (DISPLAY_HEIGHT * (12/14)) + (CREDITS_TXT_HEIGHT)):

                credits_button = True

            #Update hover text upon mouse hover
            #START button
            if start_button:
                self.interface.redraw(start_txt_hovered, (DISPLAY_WIDTH / 2) - (START_TXT_WIDTH / 2), DISPLAY_HEIGHT * (9/12))

            else:
                self.interface.redraw(start_txt, (DISPLAY_WIDTH / 2) - (START_TXT_WIDTH / 2), DISPLAY_HEIGHT * (9/12))

            #CREDITS button
            if credits_button:
                self.interface.redraw(credits_txt_hovered, (DISPLAY_WIDTH / 2) - (CREDITS_TXT_WIDTH / 2), DISPLAY_HEIGHT * (12/14))

            else:
                self.interface.redraw(credits_txt, (DISPLAY_WIDTH / 2) - (CREDITS_TXT_WIDTH / 2), DISPLAY_HEIGHT * (12/14))

            self.interface.update()

            #check for mouse click
            for event in pygame.event.get():

                if event.type == QUIT or self.exit == True:
                    return

                if event.type == MOUSEBUTTONDOWN:
                    mouse_click = True

                #check for user option selection
                if mouse_click and event.type == MOUSEBUTTONUP and start_button:
                    input_wait = False

                elif mouse_click and event.type == MOUSEBUTTONUP and credits_button:
                    input_wait = False

        if start_button:
            self.main()

        elif credits_button:
            self.credits_screen()


    '''Credits screen maintenance'''
    '''TO IMPLEMENT'''
    def credits_screen(self):
        return


    '''Game Over screen maintenance'''
    def game_over_screen(self):

        #draw the GAME OVER screen
        self.interface.redraw(self.interface.background, 0, 0)

        game_over_txt = pygame.image.load(game_over_img).convert_alpha()
        game_over_txt = pygame.transform.scale(game_over_txt, (GAME_OVER_TXT_WIDTH, GAME_OVER_TXT_HEIGHT))
        self.interface.redraw(game_over_txt, (DISPLAY_WIDTH / 2) - (GAME_OVER_TXT_WIDTH / 2), DISPLAY_HEIGHT / 3)

        restart_txt = pygame.image.load(restart_img).convert_alpha()
        restart_txt = pygame.transform.scale(restart_txt, (RESTART_TXT_WIDTH, RESTART_TXT_HEIGHT))
        restart_txt_hovered = pygame.image.load(restart_hovered_img).convert_alpha()
        restart_txt_hovered = pygame.transform.scale(restart_txt_hovered, (RESTART_TXT_WIDTH, RESTART_TXT_HEIGHT))
        self.interface.redraw(restart_txt, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

        main_menu_txt = pygame.image.load(main_menu_img).convert_alpha()
        main_menu_txt = pygame.transform.scale(main_menu_txt, (MAIN_MENU_TXT_WIDTH, MAIN_MENU_TXT_HEIGHT))
        main_menu_txt_hovered = pygame.image.load(main_menu_hovered_img).convert_alpha()
        main_menu_txt_hovered = pygame.transform.scale(main_menu_txt_hovered, (MAIN_MENU_TXT_WIDTH, MAIN_MENU_TXT_HEIGHT))
        self.interface.redraw(main_menu_txt, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

        self.interface.update()


        #wait for user input
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
                self.interface.redraw(restart_txt_hovered, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

            else:
                self.interface.redraw(restart_txt, (DISPLAY_WIDTH / 2) - (RESTART_TXT_WIDTH / 2), DISPLAY_HEIGHT * (5/9))

            #MAIN MENU button
            if main_menu_button:
                self.interface.redraw(main_menu_txt_hovered, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

            else:
                self.interface.redraw(main_menu_txt, (DISPLAY_WIDTH / 2) - (MAIN_MENU_TXT_WIDTH / 2), DISPLAY_HEIGHT * (4/6))

            pygame.display.update()


            #check for mouse click
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.exit_game()
                    return

                if event.type == MOUSEBUTTONDOWN:
                    mouse_click = True

                #check for user option selection
                if mouse_click and event.type == MOUSEBUTTONUP and restart_button:
                    input_wait = False
                    return 'restart'

                elif mouse_click and event.type == MOUSEBUTTONUP and main_menu_button:
                    input_wait = False
                    return 'main menu'

        return


    '''Main running game loop'''
    def main(self):

        #----------PYGAME GROUPS----------
        '''
        Lists to hold object instances using pygame's Sprite superclass:
            - player: player instance
            - enemy: all enemy instances
            - laser: all active laser instances (player and enemy)
            - explosion: all active explosion instances
            - powerup: all active powerup objects on the field
        '''
        player_list = pygame.sprite.Group()
        enemy_list = pygame.sprite.Group()
        laser_list = pygame.sprite.Group()
        explosion_list = pygame.sprite.Group()
        powerup_list = pygame.sprite.Group()
    
        #Attribute initialization
        #player
        player_ship = PlayerShip(player_list, 425, 400, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_HEALTH)
        player_ship.set_sprite(player_sprites[0])

        #game interface
        self.interface.set_background(space_background)
        self.interface.redraw(self.interface.background, 0, 0)
        self.interface.update_healthbar(healthbar_imgs[3])

        #initialize Game object to hold game attributes
        game = GameHandler()

        #------------------------CONTINUOUS GAME LOOP------------------------
        while(game.running):

            #run game at: 1000/90 = ~11 milliseconds per frame (90 FPS)
            pygame.time.delay(11)

            #check stdin & game variables
            for event in pygame.event.get():

                if event.type == QUIT or self.exit == True:
                    game.running = False
                    self.exit_game()
                    return

            #check for game over
            if game.game_over and game.final_explosion:
                enemy_list.clear(self.interface.display, self.interface.background)
                laser_list.clear(self.interface.display, self.interface.background)
                explosion_list.clear(self.interface.display, self.interface.background)
                player_list.clear(self.interface.display, self.interface.background)
                powerup_list.clear(self.interface.display, self.interface.background)
                selection = self.game_over_screen()

                #Restart game case
                if selection == 'restart':
                    game.game_over = False
                    game.final_explosion = True

                    #REINIT game interface
                    self.interface.set_background(space_background)
                    self.interface.update_healthbar(healthbar_imgs[3])

                    #REINIT game attributes - redraw background over sprite.Groups
                    player_ship = PlayerShip(player_list, 425, 400, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_HEALTH)
                    player_ship.set_sprite(player_sprites[0])
                    self.interface.redraw(self.interface.background, 0, 0)
                    self.interface.update()

                    #REINIT Game object and re-enter game loop
                    game = GameHandler()

                    continue

                #Return to Main Menu case
                if selection == 'main menu':
                    return

                
            #----------PLAYER MAINTENANCE----------
            #get keyboard inputs
            pressed_keys = pygame.key.get_pressed()

            #player ship movement
            if not player_ship.stunned:

                if pressed_keys[K_a] or pressed_keys[K_LEFT]:
                    if player_ship.x <= 0 - player_ship.width / 2:
                        player_ship.x = (self.interface.display_width - player_ship.width / 2)

                    else:
                        player_ship.x -= 1 * player_ship.vel

                if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
                    if player_ship.x >= (self.interface.display_width - player_ship.width / 2):
                        player_ship.x = 0 - player_ship.width / 2

                    else:
                        player_ship.x += 1 * player_ship.vel

                if pressed_keys[K_w] or pressed_keys[K_UP]:
                    if player_ship.y <= 0 + player_ship.height / 2:
                        pass
                    else:
                        player_ship.y -= 1 * player_ship.vel

                if pressed_keys[K_s] or pressed_keys[K_DOWN]:
                    if player_ship.y >= self.interface.display_height - (4 * player_ship.height) / 2:
                        pass
                    else:
                        player_ship.y += 1 * player_ship.vel

            player_ship.update_hitbox()

            
            #player ship firing sprite maintenance
            if player_ship.firing:

                player_ship.fire_frame_count += 1
                if player_ship.get_fire_frame_count() >= FIRING_FRAMES:
                    player_ship.set_sprite(player_sprites[0])
                    player_ship.firing = False
                    

            #player ship powerup maintenance
            powerup_effect_time = pygame.time.get_ticks()
            if powerup_effect_time - player_ship.get_powerup_start_time() >= PLAYER_POWERUP_DURATION:
                player_ship.remove_powerup()


            #laser firing
            if not player_ship.stunned:

                curr_fire = pygame.time.get_ticks()
                if (pressed_keys[K_RETURN] or pressed_keys[K_SPACE]) and curr_fire - player_ship.prev_fire >= player_ship.firing_interval:

                    #x-values to fire from player ship's left and right guns (visual adjustments made here)
                    player_ship.prev_fire = curr_fire
                    Laser(laser_list, player_ship.x + 4.8, player_ship.y + 15, LASER_WIDTH, LASER_HEIGHT, LASER_VEL, laser_img)
                    Laser(laser_list, player_ship.x + (player_ship.width - 6), player_ship.y + 15, LASER_WIDTH, LASER_HEIGHT, LASER_VEL, laser_img)

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

                    #laser collision - eliminates enemy and creates explosion (visually adjusted)
                    if self.is_collision(laser, enemy):
                        hit = True
                        Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                            explosion_animation, EXPLOSION_FRAMES)
                        enemy_list.remove(enemy)
                        laser_list.remove(laser)

                        #on successful hit, small chance a random powerup drops
                        if random.randint(1, 10) % 5 == 0:
                            powerup_modifier = random.choice(['bubble_shield', 'fire_rate', 'health_up', 'zap_field'])
                            PowerUp(powerup_list, enemy.x + (enemy.width/2 - POWERUP_WIDTH/2), enemy.y + (enemy.height/2 - POWERUP_HEIGHT/2),
                                POWERUP_WIDTH, POWERUP_HEIGHT, powerup_modifier, powerup_imgs[powerup_modifier], POWERUP_FRAME_DURATION)

                        break

                if hit == False:
                    laser.y -= 1 * laser.vel

                
            #----------ENEMY MAINTENANCE----------
            #spawn in enemies based on elapsed time
            interval_end = pygame.time.get_ticks()
            if interval_end - game.interval_start >= game.spawn_interval and len(enemy_list) < game.max_enemies:

                #reset spawn interval
                game.interval_start = interval_end

                #spawn enemy randomly on the field
                new_enemy = EnemyShip(enemy_list, random.randint(50, DISPLAY_WIDTH - 50), -50, ENEMY_WIDTH, ENEMY_HEIGHT)
                new_enemy.set_sprite(enemy_sprites[random.randint(0, len(enemy_sprites) - 1)])

            #update enemy positions - enemies move closer to Earth at the set velocity
            for enemy in enemy_list:

                #1 - check for enemy reaches Earth case
                if enemy.y >= DISPLAY_HEIGHT - EXPLOSION_HEIGHT / 2:
                    Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                        explosion_animation, EXPLOSION_FRAMES)
                    enemy_list.remove(enemy)
                    
                    player_ship.health -= 1

                    #check for Game Over case
                    if player_ship.health == 0:
                        game.final_explosion = False
                        game.game_over = True


                #2 - check for player ship collision case
                elif self.is_collision(player_ship, enemy):

                    #player becomes stunned and enemy ship explodes
                    player_ship.stun_player(STUN_FRAME_DURATION)
                    Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                            explosion_animation, EXPLOSION_FRAMES)
                    enemy_list.remove(enemy)

                else:
                    enemy.y += 1 * enemy.vel
                    enemy.update_hitbox()


            #----------EXPLOSION MAINTENANCE----------
            #update all explosions
            for explosion in explosion_list:

                if explosion.get_frame_count() >= EXPLOSION_FRAMES:

                    #eliminate explosion if it has completed the last frame of the animation
                    if explosion.index == len(explosion_animation) - 1:
                        explosion_list.remove(explosion)

                        #if it was the game's final explosion, game is now over
                        if game.final_explosion == False:
                            game.final_explosion = True

                        continue

                    else:
                        explosion.next_sprite()
                        continue

                explosion.frame_count += 1


            #----------POWERUP MAINTENANCE-----------
            for powerup in powerup_list:

                #start flashing powerup prior to disappearing
                if powerup.get_frame_count() <= POWERUP_FLASHING_FRAMES and not powerup.flashing:
                    powerup.flash_powerup()

                #remove when powerup expires
                elif powerup.get_frame_count() <= 0 and powerup.flashing:
                    powerup_list.remove(powerup)

                #check for player collecting powerup
                if self.is_collision(player_ship, powerup):

                    #player gains powerup effect - perform zap-field (targets enemies, not player) only if True is returned
                    if player_ship.apply_powerup(powerup.modifier):
                        for enemy in enemy_list:
                            Explosion(explosion_list, enemy.x - 2.2, enemy.y, EXPLOSION_WIDTH, EXPLOSION_HEIGHT,
                                explosion_animation, EXPLOSION_FRAMES)
                            enemy_list.remove(enemy)

                    powerup_list.remove(powerup)


            #----------FRAME UPDATING----------         

            #update the frame with all modified object attributes - last objects are drawn on top
            self.interface.redraw(self.interface.background, 0, 0)

            #if the final explosion was triggered, the explosion animation completes and rest of screen freezes
            if game.final_explosion:

                if player_ship.stunned:
                    if player_ship.get_stun_frame_count() % STUN_BLIT_RATE in (0, 1, 2, 3):
                        player_ship.redraw(self.interface)
                    player_ship.stun_frame_count -= 1
                    
                else:
                    player_ship.redraw(self.interface)

                for laser in laser_list:
                    laser.redraw(self.interface)

                for powerup in powerup_list:
                    if powerup.flashing:
                        if powerup.get_frame_count() % POWERUP_FLASH_RATE <= (POWERUP_FLASH_RATE/2):
                            powerup.redraw(self.interface)

                    else:
                        powerup.redraw(self.interface)
                    powerup.frame_count -= 1

                for enemy in enemy_list:
                    enemy.redraw(self.interface)

            for explosion in explosion_list:
                explosion.redraw(self.interface)

            #update Earth healthbar
            self.interface.update_healthbar(healthbar_imgs[player_ship.health])
            self.interface.update()

        return



    '''Method to handle game exiting.'''
    def exit_game(self):
        self.exit = True
        return



    '''Method to check if a collision between 2 game objects has occurred. Returns true on collision. Hitboxes determine the object type.'''
    def is_collision(self, object1, object2):

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
            #object 1 collision from positive y
            if object1.hitbox[1] < object2.hitbox[1] + object2.hitbox[3] and object1.hitbox[1] > object2.hitbox[1]:

                #x-values check
                if object1.hitbox[0] < object2.hitbox[0] + object2.hitbox[2] and object1.hitbox[0] + object1.hitbox[2] > object2.hitbox[0]:
                    return True

            #object 1 collision from negative y
            elif object1.hitbox[1] + object1.hitbox[3] > object2.hitbox[1] and object1.hitbox[1] < object2.hitbox[1]:

                #x-values check
                if object1.hitbox[0] < object2.hitbox[0] + object2.hitbox[2] and object1.hitbox[0] + object1.hitbox[2] > object2.hitbox[0]:
                    return True

            return False