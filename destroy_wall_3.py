#!/usr/bin/env python
import pygame
import random

def initialize():
	global res, score, width, height, brick_width, brick_height, brick_padding, paddle_width, paddle_height, paddle_x, paddle_y, paddle_vel, new_paddle, ball_radius, ball_x, ball_y, ball_vel_x, ball_vel_y, ball_acc, new_ball, brick_array
	
	res = 0
	score = str(res)
	width = 550
	height = 550

	brick_width = 20
	brick_height = 10
	brick_padding = 2

	paddle_width = 100
	paddle_height = 15
	paddle_x = (width/2)-(paddle_width/2)
	paddle_y = height - paddle_height
	paddle_vel = 0
	new_paddle = paddle(paddle_width, paddle_height, paddle_x, paddle_y, paddle_vel)

	ball_radius = 10
	ball_x = width/2
	ball_y = height - (paddle_height + ball_radius)
	ball_vel_x = 4
	ball_vel_y = -4
	ball_acc = 1
	new_ball = ball(ball_radius, ball_x, ball_y, ball_vel_x, ball_vel_y, ball_acc)

	brick_array=[]

	x=0
	y=70
	for i in range(10):
		x=0
		for j in range(25):
			new_brick = bricks(x,y,brick_width,brick_height,brick_padding)
			brick_array.append(new_brick)
			x = x + 22
		y=y+12

	brick_array.reverse()



class bricks():
	
	def __init__(self,x,y,width,height,padding):
		
		self.width = width
		self.height = height
		self.padding = padding
		self.pos_x = x
		self.pos_y = y
		self.destroy = 0
	
	def draw_brick(self, screen):
		
		if self.destroy == 0:
			pygame.draw.rect(screen,WHITE,[self.pos_x, self.pos_y, self.width, self.height])
			pygame.draw.rect(screen,BLACK,[(self.pos_x + self.width), self.pos_y ,self.padding,self.height])
			pygame.draw.rect(screen,BLACK,[self.pos_x ,(self.pos_y + self.height), self.width,self.padding])
			
			#print ("Brick drawn at",self.pos_x,self.pos_y)
	
	def set_destroy(self, val):
		
		self.destroy = val
			
	def get_width(self):
		
		return(int(self.width))
	
	def get_height(self):
		
		return(int(self.height))
		
	def get_x(self):
		
		return(int(self.pos_x))
	
	def get_y(self):
		
		return(int(self.pos_y))
	
	def get_destroy(self):
		
		return (int(self.destroy))
			
#===================================================================================================#
class paddle():
	
	def __init__(self,width,height,pos_x,pos_y,vel):
		
		self.width = width
		self.height = height
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.vel = vel

	def draw_paddle(self,screen):
		
		pygame.draw.rect(screen,WHITE,[self.pos_x, self.pos_y, self.width, self.height])
				
	def set_paddle_vel(self,new_vel):
		
		self.vel = new_vel
	
	def paddle_update(self):
		
		if ((self.pos_x + self.vel + self.width <= width) & (self.pos_x + self.vel>=0)):
			self.pos_x = self.pos_x + self.vel
		else:
			pass
			
	def get_width(self):
		
		return(int(self.width))
		
	def get_x(self):
		
		return(int(self.pos_x))
	
	def get_y(self):
		
		return(int(self.pos_y))
			
#===================================================================================================#

class ball():
	
	def __init__(self, radius, pos_x, pos_y, vel_x, vel_y, accelaration):
		
		self.radius = radius
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.acc = accelaration
		
	def draw_ball(self,screen):
		
		pygame.draw.circle(screen, WHITE, [self.pos_x, self.pos_y], self.radius)
		
	def ball_update(self, paddle=None, brick=None):
		
		#self.vel_x = self.acc * self.vel_x
		#self.vel_y = self.acc * self.vel_y
		
		self.pos_x = int(self.pos_x + self.vel_x)
		self.pos_y = int(self.pos_y + self.vel_y)
	
	
	def ball_collide_frame(self):
		
		ball_x = self.pos_x
		ball_y = self.pos_y
		ball_radius = self.radius
		
		if (((ball_x+ball_radius)>=width) | ((ball_x-ball_radius)<=0) ):
			self.vel_x*=-1
		
		if (ball_y-ball_radius<=0):
			self.vel_y*=-1	
	
	def ball_collide_paddle(self,paddle):
		
		global game_on,brick_array,s
		
		ball_x = self.pos_x
		ball_y = self.pos_y
		ball_radius = self.radius
		
		paddle_width = paddle.get_width()
		paddle_x = paddle.get_x()
		paddle_y = paddle.get_y()
		
		if ((ball_y+ball_radius)>paddle_y):
			if ((ball_x>=paddle_x) & (ball_x<=paddle_x+paddle_width)):
				self.vel_y*=-1
			else:
				game_on=0
				s.stop()
				
				
	def ball_collide_brick(self,brick_array):
		global res, score
		
		ball_x = self.pos_x
		ball_y = self.pos_y
		ball_radius = self.radius
		
		for brick in brick_array:
			brick_width = brick.get_width()
			brick_height = brick.get_height()
			brick_x = brick.get_x()
			brick_y = brick.get_y()
			if (((ball_y-ball_radius) <= (brick_y+brick_height)) & ((ball_y-ball_radius-2) <= (brick_y+brick_height))) :
				if ((ball_x>=brick_x) & (ball_x<=brick_x+brick_width)):
					brick.set_destroy(1)
					res+=1
					score=str(res)
					self.vel_y*=-1
					brick_array.remove(brick)
					break			
			 		
			 	
		return
		
	def check_bricks_left(self,brick_array):
		global game_on
		
		if (len(brick_array)==0):
			if game_on==1:
				game_on=0
			
				
		
	
	 	
#===================================================================================================#

#	250 bricks --> 10x10
#	2 pixel gap inbetween

sounds = pygame.mixer
sounds.init()

s = sounds.Sound('ricerocks.wav')
			
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

pygame.init()

# VARIABLES

game_on = 0
res = 0
score = str(res)
width = 550
height = 550

brick_width = 20
brick_height = 10
brick_padding = 2

paddle_width = width #100
paddle_height = 15
paddle_x = (width/2)-(paddle_width/2)
paddle_y = height - paddle_height
paddle_vel = 0
new_paddle = paddle(paddle_width, paddle_height, paddle_x, paddle_y, paddle_vel)

ball_radius = 10
ball_x = width/2
ball_y = height - (paddle_height + ball_radius)
ball_vel_x = 4
ball_vel_y = -4
ball_acc = 1
new_ball = ball(ball_radius, ball_x, ball_y, ball_vel_x, ball_vel_y, ball_acc)

brick_array=[]

x=0
y=70
for i in range(10):
	x=0
	for j in range(25):
		new_brick = bricks(x,y,brick_width,brick_height,brick_padding)
		brick_array.append(new_brick)
		x = x + 22
	y=y+12

brick_array.reverse()


size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Destroy Wall")

background_image = pygame.image.load("space.jpg").convert()
screen.blit(background_image, [0,0])


#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#--------- Main Program Loop ---------------------------------------------#

while not done:

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			
			if game_on==0:
				game_on=1			
				initialize()
				s.play(loops=-1)
				
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_LEFT:
				new_paddle.set_paddle_vel(-5)
			if event.key == pygame.K_RIGHT:
				new_paddle.set_paddle_vel(5)
			
			 
		if event.type == pygame.KEYUP:
			
			if event.key == pygame.K_LEFT:
				new_paddle.set_paddle_vel(0)
			if event.key == pygame.K_RIGHT:
				new_paddle.set_paddle_vel(0)		
		
	
	# GAME LOGIC
	
	new_paddle.paddle_update()
			
	new_ball.ball_collide_frame()
	new_ball.ball_collide_paddle(new_paddle)
	new_ball.ball_collide_brick(brick_array)		
	new_ball.check_bricks_left(brick_array)
	new_ball.ball_update()
	
	# CLEAR SCREEN
	#screen.fill(BLACK)
	screen.blit(background_image, [0,0])

		
	# DRAW HERE
	
	if game_on==1:
		
		pygame.mouse.set_visible(False)
		
		
		# BRICKS
		
		for each_brick in brick_array:
			each_brick.draw_brick(screen)
				
		# PADDLE
		
		new_paddle.draw_paddle(screen)
		
		# BALL
		
		new_ball.draw_ball(screen)
		
		
		#DRAW TEXT
	
		# Select the font to use. Default font, 25 pt size.
		font = pygame.font.Font(None, 50)
	
		
		# Render the text. "True" means anti-aliased text.
		# Black is the color. The variable black was defined
		# above as a list of [0,0,0]
		# Note: This line creates an image of the letters,
		# but does not put it on the screen yet.
		text = font.render("SCORE-->"+score,True,GREEN)
	
		# Put the image of the text on the screen at 250x250
		screen.blit(text, [150,15])
	
	if game_on==0:
		
		pygame.mouse.set_visible(True)
		
		
		#DRAW TEXT
	
		# Select the font to use. Default font, 25 pt size.
		font1 = pygame.font.Font(None, 80)
		font2 = pygame.font.Font(None, 30)
		# Render the text. "True" means anti-aliased text.
		# Black is the color. The variable black was defined
		# above as a list of [0,0,0]
		# Note: This line creates an image of the letters,
		# but does not put it on the screen yet.
		text1 = font2.render("Last score-->"+score,True,WHITE)
		text2 = font1.render("START",True,GREEN)
		text3 = font1.render("Destroy Wall",True,RED)
		# Put the image of the text on the screen at 250x250
		screen.blit(text1, [175,150])
		screen.blit(text2, [158,230])
		screen.blit(text3, [110,20])
		
		
	
	
	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
	
	# --- Limit to 60 frames per second
	clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

	
