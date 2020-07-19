import pygame
from pygame.locals import *
import random

class Interface:
    '''
    CLASS DESCRIPTION:
        A class to maintain and update the main game interface and pygame display attributes.

    ----------
    ATTRIBUTES:
        display - the main pygame display variable (pygame.Surface type)

        display_width - the pygame surface width
        display_height - the pygame surface height

        background - holds the game's background image

        caption - holds the game's caption displayed in the window

        healthbar - the displayed image representing Earth's current healthbar

    ----------
    METHODS:
        __init__(self, width, height):
            Creates a new screen display for the game with the passed dimensions.

        set_background(self, image):
            Sets the background class attribute and blits the background image to the display.

        set_caption(self, caption):
            Sets the game caption that appears in the overhead.

        update_healthbar(self, healthbar):
            Updates the Earth healthbar frame that appears on screen.

        redraw(self, image, x, y):
            Redraws the passed image onto the screen using pygame's Surface.blit method.

        update(self):
            Refreshes the screen to display newly drawn frame.
    '''
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height
        self.display = pygame.display.set_mode([self.display_width, self.display_height])
        self.background = None
        self.caption = None
        self.healthbar = None


    def set_background(self, image):
        self.background = pygame.image.load(image).convert()
        self.background = pygame.transform.scale(self.background, (self.display_width, self.display_height))
        self.display.blit(self.background, (0,0))

    def set_caption(self, caption):
        self.caption = caption
        pygame.display.set_caption(caption)

    def update_healthbar(self, healthbar):
        self.healthbar = pygame.image.load(healthbar).convert_alpha()
        self.healthbar = pygame.transform.scale(self.healthbar, (175, 75))
        self.display.blit(self.healthbar, ((self.display_width - 175) / 2, self.display_height - 60))
        
    def redraw(self, image, x, y):
        self.display.blit(image, (x, y))

    def update(self):
        pygame.display.update()


class GameHandler(object):
    '''
    CLASS DESCRIPTION:
        A class to maintain game variables and the current state of the game.

    ----------
    ATTRIBUTES:
        clock - pygame attribute to keep track of game time

        interval_start - holds the start time of an enemy spawn interval, and resets on every spawn
        spawn_interval - the duration between enemy spawns, initially at 5 seconds

        max_enemies - the maximum number of enemies possible in a single frame
        enemy_vel - the travel speed of all enemies on the field

        running - determines whether the game is running, and becomes False when a game-ending event occurs
        game_over - becomes True when a game-ending event occurs
        final_explosion - becomes False when a game-ending event occurs to allow the final explosion animation to complete,
            then becomes True again

    ----------
    METHODS:
        __init__(self, width, height):
            Creates a new game instance with initial game attributes.
    '''
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.interval_start = pygame.time.get_ticks()
        self.spawn_interval = 5000

        self.max_enemies = 5
        self.enemy_vel = 1

        self.running = True
        self.game_over = False
        self.final_explosion = True


class PlayerShip(pygame.sprite.Sprite):
    '''
    CLASS DESCRIPTION:
        A class holding the attributes of the player's ship.

    ----------
    ATTRIBUTES:
        x - the x-coordinate of the player's ship
        y - the y-coordinate of the player's ship

        width - the width of the player's ship
        height - the height of the player's ship

        hitbox - the rectangle created from the width and height of the player's ship that dictates collisions

        health - the remaining health of the player's ship, initially at 3

        fire_frame_count - the amount of frames that the firing sprite has been active for
        firing - boolean that becomes True during the frames that a laser is being fired

        stun_frame_count - hold the amount of frames that a player becomes stunned for
        stunned - becomes True if the player becomes stunned from enemy collision

        vel - the travel speed of the player's ship (constant)
        shield - becomes True when a player activates a shield powerup

        firing_interval - the amount of frames between laser firing for the player's ship
        prev_fire - holds the start time of the most recent laser fire

        powerup_start_time - holds the start time of an active modifier when a powerup is activated

    ----------
    METHODS:
        __init__(self, x, y, width, height):
            Creates the initial player ship and adds it to the Sprite superclass. This is only done once per game.

        set_sprite(self, sprite):
            Sets a sprite image to the player's ship.

        get_fire_frame_count(self):
            Gets the duration (in frames) that the firing effect sprite has been active for.

        update_hitbox(self):
            Updates the hitbox tuple with the modified instance attributes.

        get_stun_frame_count(self):
            Gets the amount of frames that the player has been stunned for.

        stun_player(self, frames):
            Applies a stunned state to the player's ship, where the player becomes immobilized for an amount of frames.

        apply_powerup(self, modifier):
            Applies the passed modifier to the player's ship.

        remove_powerup(self, modifier):
            Removes the passed modifier from the player's ship.

        get_powerup_start_time(self):
            Gets the start time of the currently active modifier.        

        redraw(self, display):
            Draws the updated ship onto the display object.
    '''
    def __init__(self, group, x, y, width, height, health):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.health = health

        self.sprite = None
        self.fire_frame_count = 0
        self.firing = False
        self.stun_frame_count = 0
        self.stunned = False

        self.vel = 3
        self.shield = False
        self.firing_interval = 500
        self.prev_fire = pygame.time.get_ticks()
        self.powerup_start_time = 0

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def get_fire_frame_count(self):
        return self.fire_frame_count
    
    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def get_stun_frame_count(self):
        if self.stun_frame_count == 0:
            self.stunned = False
        return self.stun_frame_count

    def stun_player(self, frames):
        self.stunned = True
        self.stun_frame_count = frames

    def apply_powerup(self, modifier):
        if modifier == 'bubble_shield':
            self.shield = True
            self.powerup_duration = pygame.time.get_ticks()
            return

        elif modifier == 'fire_rate':
            self.firing_interval /= 2
            self.powerup_duration = pygame.time.get_ticks()
            return

        elif modifier == 'health_up':
            if self.health < 3:
                self.health += 1
            return
            
        elif modifier == 'zap_field':
            return True
        return
    
    def remove_powerup(self):
        self.powerup_start_time = 0
        self.shield = False
        self.firing_interval = 500

    def get_powerup_start_time(self):
        return self.powerup_start_time

    def redraw(self, interface):
        interface.display.blit(self.sprite, (self.x, self.y))


class EnemyShip(pygame.sprite.Sprite):
    '''
    CLASS DESCRIPTION:
        An object class for instances of enemy ships.

    ----------
    ATTRIBUTES:
        x - the x-coordinate of the enemy ship, which will not change after initialization
        y - the y-coordinate of the enemy ship, which will increase consistently

        width - the width of the enemy ship
        height - the height of the enemy ship

        hitbox - the rectangle created from the width and height of the enemy ship that dictates collisions

    ----------
    METHODS:
        __init__(self, x, y, width, height):
            Creates an instance of the enemy ship and adds it to the Sprite superclass. Done once per enemy ship spawn.

        set_sprite(self, sprite):
            Sets a sprite image to the enemy ship, selected from a list of enemy sprites.

        update_hitbox(self):
            Updates the hitbox tuple with the modified instance attributes.

        redraw(self, display):
            Draws the updated enemy ship onto the display object.        
    '''
    def __init__(self, group, x, y, width, height):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprite = None
        self.vel = 1

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def redraw(self, interface):
        interface.display.blit(self.sprite, (self.x, self.y))
        


class Laser(pygame.sprite.Sprite):
    '''
    CLASS DESCRIPTION:
        An object class for instances of laser beams being fired.

    ----------
    ATTRIBUTES:
        x - the x-coordinate of the laser, which will not change after firing
        y - the y-coordinate of the laser, which will decrease at the rate of its velocity
        init_y - the initial y-coordinate of the laser, used to 

        width - the width of the laser, which dictates its hitbox
        vel - the velocity of the laser (constant)

        hit - boolean that turns True upon collision with an enemy

        sprite - holds the image of the laser to be displayed

    ----------
    METHODS:
        __init__(self, x, y, vel):
            Creates an instance of the laser beam and adds it to the Sprite superclass. Done once per laser fired.

        set_sprite(self, sprite):
            Sets a sprite image to the laser beam.

        get_travel(self):
            Gets the distance traveled by the laser.

        redraw(self, display):
            Draws the updated laser onto the display object.
    '''
    def __init__(self, group, x, y, width, height, vel, sprite):
        super().__init__(group)
        self.x = x
        self.y = y
        self.init_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hit = False
        self.set_sprite(sprite)

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, 15))

    def get_travel(self):
        return abs(self.y - self.init_y)

    def redraw(self, interface):
        interface.display.blit(self.sprite, (self.x, self.y))



class Explosion(pygame.sprite.Sprite):
    '''
    CLASS DESCRIPTION:
        An object class for instances of explosions that occur after collisions.

    ----------
    ATTRIBUTES:
        x - the x-coordinate of the explosion
        y - the y-coordinate of the explosion

        width - the width of the explosion
        height - the height of the explosion

        frame_count - hold the number of frames that the current sprite has been active for
        sprites - a list of sprites that create the explosion animation
        index - the index of the current sprite in sprites list
        curr_sprite - holds the current image of the explosion to be displayed

    ----------
    METHODS:
        __init__(self, group, x, y, width, height, sprites, duration):
            Creates an instance of an explosion and adds it to the Sprite superclass. Done once per enemy removal.

        get_frame_count(self):
            Gets the duration (in frames) that the individual explosion sprite has been active for.

        next_sprite(self):
            Sets the next sprite of the explosion to continue the animation.

        redraw(self, interface):
            Draws the updated explosion onto the display object.
    '''
    def __init__(self, group, x, y, width, height, sprites, duration):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.frame_count = 0
        self.sprites = sprites
        self.index = 0
        self.curr_sprite = pygame.image.load(self.sprites[self.index]).convert_alpha()

    def get_frame_count(self):
        return self.frame_count
        
    def next_sprite(self):
        self.index += 1
        self.curr_sprite = pygame.image.load(self.sprites[self.index]).convert_alpha()
        self.frame_count = 0

    def redraw(self, interface):
        interface.display.blit(self.curr_sprite, (self.x, self.y))


class PowerUp(pygame.sprite.Sprite):
    '''
    CLASS DESCRIPTION:
        An object class for instances of powerups that have a chance to spawn after eliminated enemies.

    ----------
    ATTRIBUTES:
        x - the x-coordinate of the powerup, taken from the coordinate of the eliminated enemy
        y - the y-coordinate of the powerup, taken the coordinate of the eliminated enemy

        width - the width of the powerup
        height - the height of the powerup

        hitbox - the rectangle created from the width and height of the powerup that dictates collisions

        modifier - the type of powerup being created
        sprite - holds the image of the powerup to be displayed

        frame_count - the total duration (in frames) that the powerup will appear on the field for
        flashing - boolean that turns True if the powerup is about to despawn

    ----------
    METHODS:
        __init__(self, group, x, y, width, height, sprites, duration):
            Creates an instance of a powerup and adds it to the Sprite superclass. Done once per powerup spawn.

        set_sprite(self, sprite):
            Sets a sprite image to the powerup, determined by its modifier.

        get_frame_count(self):
            Gets the current frame count of the powerup.

        flash_powerup(self):
            Sets the powerup to a flashing state before it despawns.

        redraw(self, interface):
            Draws the updated powerup onto the display object.
    '''
    def __init__(self, group, x, y, width, height, modifier, sprite, frames):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)

        self.modifier = modifier
        self.set_sprite(sprite)

        self.frame_count = frames
        self.flashing = False

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def get_frame_count(self):
        if self.frame_count == 0:
            self.flashing = False
        return self.frame_count

    def flash_powerup(self):
        self.flashing = True

    def redraw(self, interface):
        interface.display.blit(self.sprite, (self.x, self.y))

