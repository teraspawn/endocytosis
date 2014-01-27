#! /usr/bin/python

import pygame, sys, math

def cv(number):
	number = (number*40)+40
	return number

def ch(number):
	number = (number*20)+20
	return number

pygame.init()

bent = []
bentfile = open('output/output-bent')
for item in bentfile:
	item = item.split()
	bent.append(item[1:])

barrier = []
barrierfile = open('output/output-barriernumber')
for item in barrierfile:
	item = item.split()
	barrier.append(float(item[1]))

filaments = []
filamentsfile = open('output/output-length')
for item in filamentsfile:
	item = item.split()
	filaments.append(item[1:])

bundling = []
bundlingfile = open('output/output-bundling')
for item in bundlingfile:
	item = item.split()
	bundling.append(item[1:])
noofbuns = len(bundling[0])/3

nooffils = int(len(filaments[0]))
boundary = int(math.ceil(max(barrier)))

size = width, height = ch(boundary)+20, cv(nooffils)+20
red = 255, 0, 0
blue = 0, 0, 255
black = 0,0,0
white = 255,255,255

screen = pygame.display.set_mode(size)

tmax = len(barrier)

while 1:
	screen.fill(black)
	for i in range(0,tmax):
		# allow exit
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		# draw leftmost membrane
		pygame.draw.line(screen, red, [20, 20], [20, cv(nooffils)], 3)
		# draw rightmost membrane
		pygame.draw.line(screen, red, [ch(barrier[i]),20], [ch(barrier[i]),cv(nooffils)],3)
		x = 40
		for item in range(0,len(filaments[i])):
			length = float(filaments[i][item])
			start = ch(barrier[i]) - length*20
			pygame.draw.line(screen, blue, [start,x], [ch(barrier[i]),x],3)
			vertical = float(bent[i][item])
			#print vertical
			curve = pygame.Rect(start-5, x, (ch(barrier[i])-start), vertical)
#			pygame.draw.arc(screen,blue,curve,math.pi/2, math.pi)
			x += 40
		for a in range(0,noofbuns):
			if bundling[i][3*a] != "a":
				distance = ch(int(barrier[i])) - int(10*(float(bundling[i][3*a])))
				first = cv(int(bundling[i][3*a+1]))
				second = cv(int(bundling[i][3*a+2]))
				crcolor = 255,255,int(a)*25
				pygame.draw.circle(screen,crcolor ,[distance,first], 3)
				pygame.draw.circle(screen,crcolor ,[distance,second], 3)
				pygame.draw.line(screen,crcolor ,[distance,first],[distance,second],3)
		pygame.display.flip()
		pygame.time.delay(300)
		screen.fill(black)
		
