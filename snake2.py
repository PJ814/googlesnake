import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
	def __init__(self):
		#code to track location and direction
		self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False 
		
		#code to load snake body
		# since this is repetative code, we will code the first line together, then i'll give them to you
		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()
		
		# code that loads correct snake part/image to correct place
		# to save time, this will be given to you
		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)
	
	def update_head_graphics(self):
		#change head depending on direction (left right up or down)
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1, 0):
			self.head = self.head_left
		elif head_relation == Vector2(-1, 0):
			self.head = self.head_right
		elif head_relation == Vector2(0, 1):
			self.head = self.head_up
		elif head_relation == Vector2(0, -1):
			self.head = self.head_down

	def update_tail_graphics(self):
		#change tail depending on direction (left right up or down))
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1, 0):
			self.tail = self.tail_left
		elif tail_relation == Vector2(-1, 0):
			self.tail = self.tail_right
		elif tail_relation == Vector2(0, 1):
			self.tail = self.tail_up
		elif tail_relation == Vector2(0, -1):
			self.tail = self.tail_down
			
	def move_snake(self):
		#move snake
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False 
		else: 
			body_copy = self.body[:-1]
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		#set new block to True 
		self.new_block = True 

	def reset(self):
		#set reset location
		self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
		self.direction = Vector2(0,0)

class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)
		#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
	def __init__(self):
		# make snake and fruit appear in game
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		#use functions that we created to make things appear
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()

	def check_collision(self):
		#check to see if snake touched fruit 
		#if true, make fruit randomly appear again somewhere else
		if self.fruit.pos == self.snake.body[0]:
			while True:
				self.fruit.randomize()
				if self.fruit.pos not in self.snake.body:
					break
			self.snake.add_block()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		#reset snake position
		self.snake.reset()
  
    #this function will create the checkerboard effect in the game
	# to save time, this will be explained through example from a previous game that was made
    # then given to you.
	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		#create variables necessary for score 
		score_text = str(len(self.snake.body) - 3)
		score_surface = font.render(score_text, True, (56,74,12))
		score_x = int(cell_size *  cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
  
		#draw all parts of score
		pygame.draw.rect(screen, (167, 205, 61), bg_rect)
		screen.blit(apple, apple_rect)
		screen.blit(score_surface, score_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 250)

main = MAIN()
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		#screen update
		if event.type == SCREEN_UPDATE:
			main.update()
   
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main.snake.direction.y != 1:
					main.snake.direction = Vector2(0, -1)
			if event.key == pygame.K_DOWN:
				if main.snake.direction.y != -1:
					main.snake.direction = Vector2(0, 1)
			if event.key == pygame.K_LEFT:
				if main.snake.direction.x != 1:
					main.snake.direction = Vector2(-1, 0)
			if event.key == pygame.K_RIGHT:
				if main.snake.direction.x != -1:
					main.snake.direction = Vector2(1, 0)

	screen.fill((175,215,70))
	main.draw_elements()
	pygame.display.update()
	clock.tick(60)