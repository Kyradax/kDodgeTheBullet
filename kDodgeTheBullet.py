#Kyradax's spaceInvaders

VERSION = "0.3"

try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from socket import *
        from pygame.locals import *
	from menu import *
except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)

def load_png(name):
        """ Load image and return image object"""
        fullname = os.path.join('data', name)
        try:
                image = pygame.image.load(fullname)
                if image.get_alpha is None:
                        image = image.convert()
                else:
                        image = image.convert_alpha()
        except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
        return image, image.get_rect()

#bullet class
class bullet(pygame.sprite.Sprite):
        """A ball that will move across the screen
        Returns: ball object
        Functions: update, calcnewpos
        Attributes: area, vector"""

        def __init__(self, (xy), vector):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = load_png('bullet.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.vector = vector

        def update(self):
                newpos = self.calcnewpos(self.rect,self.vector)
                self.rect = newpos
		(angle,z) = self.vector

		if not self.area.contains(newpos):
			tl = not self.area.collidepoint(newpos.topleft)
			tr = not self.area.collidepoint(newpos.topright)
			bl = not self.area.collidepoint(newpos.bottomleft)
			br = not self.area.collidepoint(newpos.bottomright)
			if tr and tl or (br and bl):
				angle = -angle
			if tl and bl:
				angle = math.pi - angle
			if tr and br:
				angle = math.pi - angle
		else:
			
			if self.rect.colliderect(player.rect) == 1:
				main()
		self.vector = (angle,z)

        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
                return rect.move(dx,dy)

#player's ship class
class kShip(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png('kShip.png')
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.speed = 10
		self.state = "still"
		self.reinit()

	def reinit(self):
		self.state = "still"
		self.movepos = [0,0]
		self.rect.center = self.area.center

	def update(self):
		newpos = self.rect.move(self.movepos)
		if self.area.contains(newpos):
			self.rect = newpos
		pygame.event.pump()

	def moveup(self):
		self.movepos[1] = self.movepos[1] - (self.speed)
		self.state = "moveup"

	def movedown(self):
		self.movepos[1] = self.movepos[1] + (self.speed)
		self.state = "movedown"

	def moveleft(self):
		self.movepos[0] = self.movepos[0] - (self.speed)
		self.state = "moveleft"

	def moveright(self):
		self.movepos[0] = self.movepos[0] + (self.speed)
		self.state = "moveright"

def main():

	#centers the window on the computer screen
	os.environ['SDL_VIDEO_CENTERED'] = '1'

        #initialise screen
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('kDodgeTheBullet')

	#play music
	pygame.mixer.music.load('data/babyPiano.ogg')
	pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
	pygame.mixer.music.play(-1) #-1 means it plays forever

	#fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	#set caption
	fontPath = 'data/coders_crux.ttf'
	font0 = pygame.font.Font(fontPath, 72)
	text0 = font0.render("kDodgeTheBullet", 1, (255, 255, 255))
	textpos0 = text0.get_rect(center = (400, 100))
	background.blit(text0, textpos0)
	font1 = pygame.font.Font(fontPath, 36)
	text1 = font1.render("press ENTER to continue", 1, (255, 255, 255))
	textpos1 = text1.get_rect(center = (400, 300))
	background.blit(text1, textpos1)

	#state variables
	state = 0
	prevState = 1
	start0 = 0
	start1 = 0
	dead = 0

	#ignore mouse motion (greatly reduces resources when not needed)
	pygame.event.set_blocked(pygame.MOUSEMOTION)

	while start0 == 0:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_RETURN:
					start0 = 1		
		screen.blit(background, (0, 0))
		pygame.display.flip()

	#deleting caption
	background.fill((0,0,0))
	screen.blit(background, (0, 0))
	pygame.display.flip()

	#setting menu
	menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
		[('Start Game', 1, None),
		('Options',    2, None),
		('Exit',       3, None)])
	menu.set_center(True, True)
	menu.set_alignment('center', 'center')

	#rect_list is the list of pygame.Rect's that will tell pygame where to
	#update the screen (there is no point in updating the entire screen if only
	#a small portion of it changed!)
	rectList = []

	#menu loop
	while start1 == 0:
		#check if the state has changed, if it has, then post a user event to
		#the queue to force the menu to be shown at least once
		if prevState != state:
			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prevState = state
		#get the next event
		e = pygame.event.wait()
		#update the menu, based on which "state" we are in - When using the menu
		#in a more complex program, definitely make the states global variables
		#so that you can refer to them by a name
		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				rectList, state = menu.update(e, state)
			elif state == 1:
#				print 'Start Game!'
				start1 = 1
			elif state == 2:
#				print 'Options!'
				state = 0
			else:
#				print 'Exit!'
				pygame.quit()
				sys.exit()
		#quit if the user presses the exit button
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		#update the screen
		pygame.display.update(rectList)

	#deleting menu
	screen.blit(background, (0, 0))
	pygame.display.flip()

	#initializing player
	global player
	player = kShip()
	playersprite = pygame.sprite.RenderPlain(player)

	#initializing ball
#	random.seed()
#	s = (random.randint(1,9))
#	a = (random.randint(0,10))
#	x = (random.sample([0, 800], 1))
#	y = (random.sample([0, 600], 1))
	bul = bullet((0, 0), (0.47, 13))
	bulsprite = pygame.sprite.RenderPlain(bul)

	#initialise clock
	clock = pygame.time.Clock()

	while dead == 0:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					player.moveleft()
				if event.key == K_RIGHT:
					player.moveright()
				if event.key == K_UP:
					player.moveup()
				if event.key == K_DOWN:
					player.movedown()
			elif event.type == KEYUP:
#				if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_UP:
#					player.movepos = [0,0]
#					player.state = "still"
				if event.key == K_LEFT or event.key == K_RIGHT:
					player.movepos[0] = 0
					player.state = "stillX"
				elif event.key == K_DOWN or event.key == K_UP:
					player.movepos[1] = 0
					player.state = "stillY"


		screen.blit(background, player.rect)
		screen.blit(background, bul.rect)
		playersprite.update()
		bulsprite.update()
		playersprite.draw(screen)
		bulsprite.draw(screen)
		pygame.display.flip()

if __name__ == "__main__":
	main()
