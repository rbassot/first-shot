import pygame
from pygame.locals import *

class Interface:
    '''
    CLASS DESCRIPTION:
        A class to maintain and update the main game interface and display attributes.

    ----------
    ATTRIBUTES:
        display - the main pygame display variable (pygame.Surface)

        display_width - the pygame surface width
        display_height - the pygame surface height

        background - holds the game's background image

        caption - holds the game's caption

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

        redraw(self):
            Refreshes the contents of the screen using pygame's Surface.blit method.

    '''
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
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
        firing - boolean that becomes true during the frames that a laser is being fired

    ----------
    METHODS:
        __init__(self, x, y, width, height):
            Draws the initial player ship and adds it to the Sprite superclass. This is only done once per game.

        set_sprite(self, sprite):
            Sets a sprite image to the player's ship.

        get_fire_frame_count(self):
            Gets the duration (in frames) that the firing effect sprite has been active for

        update_hitbox(self):
            Updates the hitbox tuple with the modified instance attributes.

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

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def get_fire_frame_count(self):
        return self.fire_frame_count
    
    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def redraw(self, display):
        display.display.blit(self.sprite, (self.x, self.y))


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
            Draws an instance of the enemy ship and adds it to the Sprite superclass. Done once per enemy ship spawn.

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

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def redraw(self, display):
        display.display.blit(self.sprite, (self.x, self.y))
        


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

        hit - boolean that turns true upon collision with an enemy

        sprite - holds the image of the laser to be displayed

    ----------
    METHODS:
        __init__(self, x, y, vel):
            Draws an instance of the laser beam and adds it to the Sprite superclass. Done once per laser fired.

        set_sprite(self, sprite):
            Sets a sprite image to the laser beam.

        get_travel(self):
            Gets the distance traveled by the laser.

        update_hitbox(self):
            Updates the hitbox tuple with the modified instance attributes.

        redraw(self, display):
            Draws the updated laser onto the display object.
    '''

    def __init__(self, group, x, y, width, height, vel):
        super().__init__(group)
        self.x = x
        self.y = y
        self.init_y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hit = False
        self.sprite = None

    def set_sprite(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, 15))

    def get_travel(self):
        return abs(self.y - self.init_y)

    def redraw(self, display):
        display.display.blit(self.sprite, (self.x, self.y))



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
        curr_sprite - holds the image of the explosion to be displayed 
    .................
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

    def redraw(self, display):
        display.display.blit(self.curr_sprite, (self.x, self.y))