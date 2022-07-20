import pygame
import pickle
from os import path

#Initialize all imported pygame modules
pygame.init()

#Creating fps counter for the level editor
clock = pygame.time.Clock()
fps = 60

#Creating/Defining game window
block_size = 50
cols = 20
margin = 100
display_width = 1000
display_height = 800

#Using pygame_set_mode function to create display variable
display = pygame.display.set_mode((display_width, display_height))
#Using pygame.set_caption function to name the game window
pygame.display.set_caption('Level Designer')


#loading in the png images
Real_Sun = pygame.image.load('img/Real_Sun.png')
Real_Sun = pygame.transform.scale(Real_Sun, (block_size, block_size))
Background = pygame.image.load('img/sky.png')
Background = pygame.transform.scale(Background, (display_width, display_height - margin))
Grass_block = pygame.image.load('img/Grass_block.png')
Dirt_block = pygame.image.load('img/Dirt_block.png')
Bitcoin = pygame.image.load('img/Bitcoin.png')
platform_x = pygame.image.load('img/platform_x.png')
platform_y = pygame.image.load('img/platform_y.png')
Real_lava = pygame.image.load('img/Real_lava.png')
Enemy = pygame.image.load('img/Enemy.png')
Exit = pygame.image.load('img/Exit.png')
Save = pygame.image.load('img/Save_btn.png')
load = pygame.image.load('img/load_btn.png')


#defining game variables
#We only need these two variables because this designer is based on blocks and clicks
#Clicked must be set to false from default and it will be set to true later in the script if clicked
#level must be set equal to 1 by deafult, this ensures each time the designer is loaded up it will start from level1
clicked = False
level = 1

#defining the colors
white = (255, 255, 255)
baby_blue = (137, 207, 240)

font = pygame.font.SysFont('Futura', 24)

#creating an empty box list
#This is so the world designer begins with a fresh and blank world to work with
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#Creating boundary
for block in range(0, 20):
	world_data[19][block] = 2
	world_data[0][block] = 1
	world_data[block][0] = 1
	world_data[block][19] = 1

#Defining the world designer
def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#Dirt_block blocks
					img = pygame.transform.scale(Dirt_block, (block_size, block_size))
					display.blit(img, (col * block_size, row * block_size))
				if world_data[row][col] == 2:
					#Grass_block blocks
					img = pygame.transform.scale(Grass_block, (block_size, block_size))
					display.blit(img, (col * block_size, row * block_size))
				if world_data[row][col] == 3:
					#Enemy blocks
					img = pygame.transform.scale(Enemy, (block_size, int(block_size * 0.75)))
					display.blit(img, (col * block_size, row * block_size + (block_size * 0.25)))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x, (block_size, block_size // 2))
					display.blit(img, (col * block_size, row * block_size))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y, (block_size, block_size // 2))
					display.blit(img, (col * block_size, row * block_size))
				if world_data[row][col] == 6:
					#Real_lava
					img = pygame.transform.scale(Real_lava, (block_size, block_size // 2))
					display.blit(img, (col * block_size, row * block_size + (block_size // 2)))
				if world_data[row][col] == 7:
					#Bitcoin
					img = pygame.transform.scale(Bitcoin, (block_size // 2, block_size // 2))
					display.blit(img, (col * block_size + (block_size // 4), row * block_size + (block_size // 4)))
				if world_data[row][col] == 8:
					#Exit
					img = pygame.transform.scale(Exit, (block_size, int(block_size * 1.5)))
					display.blit(img, (col * block_size, row * block_size - (block_size // 2)))

#This section draws a grid aroud each block so it is easier to customize the level
def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(display, white, (c * block_size, 0), (c * block_size, display_height - margin))
		#horizontal lines
		pygame.draw.line(display, white, (0, c * block_size), (display_width, c * block_size))

#function for outputting text onto the screen you can now call draw_text and use it anywhere in the script
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	display.blit(img, (x, y))

#Button class for each menu button
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		display.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and Save buttons
Save_button = Button(display_width // 2 - 150, display_height - 80, Save)
load_button = Button(display_width // 2 + 50, display_height - 80, load)

#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	display.fill(baby_blue)
	display.blit(Background, (0, 0))
	display.blit(Real_Sun, (block_size * 2, block_size * 2))

	#load and Save level
	if Save_button.draw():
		#Save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level blocks
	draw_world()
	draw_grid()


	#text showing current level
	draw_text(f'Level: {level}', font, white, block_size, display_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, block_size, display_height - 40)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change blocks
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // block_size
			y = pos[1] // block_size
			#check that the coordinates are within the block area
			if x < 20 and y < 20:
				#update block value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game screen window
	pygame.display.update()

pygame.quit()
