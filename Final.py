import pygame
import pickle
from pygame import mixer
from os import path

#Initialize all imported mixer and pygame modules
mixer.init()
pygame.init()

#Setting up fps counter for game using the pygame time clock function
clock = pygame.time.Clock()
fps = 60

#Setting the display ratio varibles
display_width = 1000
display_height = 800

#Using the pygame display function to set the display equal to the two previously set variables
display = pygame.display.set_mode((display_width, display_height))
#Setting the name of the game display window
pygame.display.set_caption('Final Project')

#define font using the pygame font function
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#defining colors
red = (255, 0, 0)
White = (255, 255, 255)

#Defining basic game variables
block_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 3
score = 0

#Loading in the .PNG images
Real_Sun = pygame.image.load('img/Real_Sun.png')
Background = pygame.image.load('img/sky.png')
restart = pygame.image.load('img/restart_btn.png')
start = pygame.image.load('img/start_btn.png')
exit = pygame.image.load('img/exit_btn.png')

#Loading in and setting the volume for the .WAV sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
bitcoin_fx = pygame.mixer.Sound('img/bitcoin.wav')
#Using .set_volume function to decrease the max of the original audio
bitcoin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)

#function to reset the level
def reset_level(level):
    sprite.reset(100, display_height - 130)
    #emptying out each of the groups for reset
    enemy_group.empty()
    platform_group.empty()
    real_lava_group.empty()
    exit_group.empty()

    #load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        #using pick.load to load in level data generated from the level_maker
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world

#Draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    #display.blit copies the image from one surface to another
    display.blit(img, (x, y))

#World class to define the attributes within the world
class World():
    def __init__(self, data):
        self.block_list = []


        #loading the World pictures
        Dirt_block = pygame.image.load('img/Dirt_block.png')
        Grass_block = pygame.image.load('img/Grass_block.png')

        #Setting the images into a drawable form, i.e. 1 equals Dirt_block block, 2 equals Grass_block block etc...
        row_count = 0
        for row in data:
            col_count = 0
            for block in row:
                #Dirt_block
                if block == 1:
                    #Transforming the image to fit the blocks
                    img = pygame.transform.scale(Dirt_block, (block_size, block_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * block_size
                    img_rect.y = row_count * block_size
                    block = (img, img_rect)
                    self.block_list.append(block)
                #Grass_block
                if block == 2:
                    img = pygame.transform.scale(Grass_block, (block_size, block_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * block_size
                    img_rect.y = row_count * block_size
                    block = (img, img_rect)
                    self.block_list.append(block)
                #Enemy
                if block == 3:
                    enemy = Enemy(col_count * block_size, row_count * block_size + 5)
                    enemy_group.add(enemy)
                #Platform1
                if block == 4:
                    platform = Platform(col_count * block_size, row_count * block_size, 1, 0)
                    platform_group.add(platform)
                #PLatform2
                if block == 5:
                    platform = Platform(col_count * block_size, row_count * block_size, 0, 1)
                    platform_group.add(platform)
                #Real_lava
                if block == 6:
                    real_lava = Real_lava(col_count * block_size, row_count * block_size + (block_size // 2))
                    real_lava_group.add(real_lava)
                #Bitcoin
                if block == 7:
                    bitcoin = Bitcoin(col_count * block_size // 2, row_count * block_size + (block_size // 2))
                    bitcoin_group.add(bitcoin)
                #Exit
                if block == 8:
                    exit = Exit(col_count * block_size, row_count * block_size - (block_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1

    def draw(self):
        for block in self.block_list:
            display.blit(block[0], block[1])

#sprite class where we define the player and it's attibutes
class Sprite():
    #Initializing the sprite
    def __init__(self, x, y):
        self.reset(x, y)
    #this section is needed for when the sprite dies. This fuction tells the game to place the player back to the starting position in the case of a game over.
    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20
        
        if game_over == 0:
            #Defining the keypresses
            key = pygame.key.get_pressed()
            #Space Key
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                #Defines how high the player jumps
                self.vel_y = -15
                self.jumped = True
                #This line is added to allow the player to jump multiple times
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            #Left Key
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            #Right key
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            #Neither Left or Right key pressed
            #This section allows the character to remain in the position it was last facing when user let go of the keys.
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #handles animations
            #if statements to determine the sprites animation depending on the self. variable
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for world collisions
            self.in_air = True
            for block in world.block_list:
                #check for collision in x direction
                if block[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if block [1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = block[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = block[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #checks for collision with enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
                #plays the game over sound when colliding with enemies
                game_over_fx.play()

            #checks for collision with real_lava
            if pygame.sprite.spritecollide(self, real_lava_group, False):
                game_over = -1
                game_over_fx.play()

            #checks for collision with finish/exit. If character enters exit initialize exit_group
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #checks for collision with platforms. Since the platforms arent stationary this section is more complex
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #checks if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #checks if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            #updates sprite coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over ==-1:
            self.image = self.dead_image
            draw_text('Game OVER!', font, red, (display_width // 2) - 200, display_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #draws sprite onto display
        display.blit(self.image, self.rect)

        return game_over

    #This section defines how the sprite rests after the game is over or when the sprite dies
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        # Load images
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

#class for each button or selection icon
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #Gets the mouse position
        pos = pygame.mouse.get_pos()

        #Checks mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                print('CLICKED')
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #Draw the button
        display.blit(self.image, self.rect)

        return action

#class to define the enemy sprite and its atrributes
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    #This section defines enemy movement in the game i.e. moving back and forth.
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

#Platform class that defines the attributes for the platform blocks
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (block_size, block_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
    
    #This section also defines the platform movement the same way as we did for the enemies.
    #The only difference in this part compared to the enemies is the addition of moving along the y-axis
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

#Lava class for defining the attributes that make up the lava blocks
class Real_lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/real_lava.png')
        #Transforming block size to fit accordingly
        self.image = pygame.transform.scale(img, (block_size, block_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Bitcoin class for defining the atrributes that make up the Bitcoin blocks
class Bitcoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/bitcoin.png')
        #Transforming the block size to fit accordingly
        self.image = pygame.transform.scale(img, (block_size // 2, block_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

#Exit class for defining the exit or finish of each level
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (block_size, block_size * 1.55))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Creating an instance of the sprite class
sprite = Sprite(100, display_height - 130)

enemy_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
real_lava_group = pygame.sprite.Group()
bitcoin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Creating bitcoin logo for showing the score
bitcoin_score = Bitcoin(block_size // 2, block_size // 2)
bitcoin_group.add(bitcoin_score)

#load in level data and create world
#The level data is created fom Level_designer.py, which makes it much easier/cleaner than manually coding a world.
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#Creating buttons for menu
start_button = Button(display_width // 2 - 350, display_height //2, start)
exit_button = Button(display_width // 2 - 0, display_height //2, exit)
restart_button = Button(display_width // 2 - 50, display_height // 2 + 100, restart)
run = True

#Game loop that keeps the game window running
while run:
    #Sets the clock tick equal 60, i.e. fps
    clock.tick(fps)

    #While the window is runnning display thenbackground and the sun using the .blit function
    #It is important to put the background first
    display.blit(Background, (0,0))
    display.blit(Real_Sun, (85, 50))

    #
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        world.draw()

        if game_over == 0:
            enemy_group.update()
            platform_group.update()
            #check if a bitcoin has been collected
            if pygame.sprite.spritecollide(sprite, bitcoin_group, True):
                #update score
                score += 1
                #Play bitcoin sound effect if the sprite collides with a bitcoin.
                bitcoin_fx.play()
            draw_text('X ' + str(score), font_score, White, block_size - 10, 10)

        #This section draws out each defined element of the game.
        #Without this section the game would not draw any of the items onto the display
        enemy_group.draw(display)
        platform_group.draw(display)
        real_lava_group.draw(display)
        bitcoin_group.draw(display)
        exit_group.draw(display)

        game_over = sprite.update(game_over)

        #if sprite has died
        if game_over == -1:
            if restart_button.draw():
                sprite.reset(100, display_height - 130)
                game_over = 0
                score = 0

        #if sprite beats the level
        if game_over == 1:
            #Go to next level
            level += 1
            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
            #The else statement is needed when you complete the last level
            else:
                draw_text('Final Project | LIS4930 | Robert Moncrief', font, red, (display_width // 2) - 460, display_height // 2)
                #add restart button, if restart button is pressed set the level back to 1
                #Clear the world and set the level back to 1
                if restart_button.draw():
                    level = 1
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0

    #Setting up a quit option for the game, without this there would be no way of exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
