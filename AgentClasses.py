import pygame
import math
from random import randint

def angle2XY(lineLen, angle):
	x=y=lineLen
	while angle > 360:
		angle=angle-360
	while angle<0:
		angle=angle+360
	x *= math.sin(math.radians(90-angle))
	y *= math.sin(math.radians(angle))
	return [x,y]
def triangleArea(x1,y1,x2,y2,x3,y3):
	return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


class Agent:
	def __init__(self, screen, radius=10, pos=[0,0], color=(255,0,0), sightLen=50, seperation=50, moveLen=5, screenSize=[500,500]):
		self.seperation = seperation
		self.sightLen = sightLen
		self.pos = pos
		self.radius = radius
		self.moveLen = moveLen
		self.angle = 90
		self.color=color
		self.screen = screen
		self.screenSize = screenSize
	def rotate(self,direction):
		if direction == "right":
			if self.angle >= 355:
				self.angle = 0
			else:
				self.angle+=5
		else:
			if self.angle <= 5:
				self.angle = 360
			else:
				self.angle-=5
	def move(self,direction):
		xMove, yMove = angle2XY(self.moveLen,self.angle)
		xMove = round(xMove)
		yMove = round(yMove)
		if direction == "forward":
			self.pos[0] += xMove
			self.pos[1] += yMove
		elif direction == "back":
			self.pos[0] -= xMove
			self.pos[1] -= yMove
	def draw(self):
		pygame.draw.circle(self.screen, self.color, self.pos, self.radius)
		x1,y1 = angle2XY(self.sightLen,self.angle + 15)
		pygame.draw.line(self.screen,(255,255,255),(self.pos[0],self.pos[1]),(math.floor(self.pos[0]+x1),math.floor(self.pos[1]+y1)))
		x2,y2 = angle2XY(self.sightLen,self.angle - 15)
		pygame.draw.line(self.screen,(255,255,255),(self.pos[0],self.pos[1]),(math.floor(self.pos[0]+x2),math.floor(self.pos[1]+y2)))
	def seeFood(self,foodPelletList):
		foodSaw = 0
		x1,y1 = angle2XY(self.sightLen,self.angle + 15) #a
		x2,y2 = angle2XY(self.sightLen,self.angle - 15) #b
		x1+=self.pos[0]
		x2+=self.pos[0]
		y1+=self.pos[1]
		y2+=self.pos[1]
		x3,y3 = self.pos 								#c
		for pellet in foodPelletList.food:
			# p is point, abc are points on triangle
			Aabc = triangleArea(x1,y1,x2,y2,x3,y3)
			Aabp = triangleArea(x1,y1,x2,y2,pellet.x,pellet.y)
			Aacp = triangleArea(x1,y1,x3,y3,pellet.x,pellet.y)
			Abcp = triangleArea(x2,y2,x3,y3,pellet.x,pellet.y)

			if Aabc == Aabp + Aacp + Abcp:
				foodSaw = 1
				break
		return foodSaw
	def seeWall(self):
		x1,y1 = angle2XY(self.sightLen,self.angle + 15)
		x2,y2 = angle2XY(self.sightLen,self.angle - 15)
		x1+=self.pos[0]
		x2+=self.pos[0]
		y1+=self.pos[1]
		y2+=self.pos[1]
		if x1<0 or y1<0 or x2<0 or y2<0 or x1>self.screenSize[0] or y1>self.screenSize[1] or x2>self.screenSize[0] or y2>self.screenSize[1]:
			return 1
		else:
			return 0



class food:
	def __init__(self,x,y):
		self.x = randint(0,x)
		self.y = randint(0,y)

class foodPellets:
	def __init__(self,screen,screenSize=[500,500],count=100,radius=2):
		self.food = []
		self.radius=radius
		self.screen = screen
		for x in range(count):
			self.food.append(food(screenSize[0],screenSize[1]))
	def eatPellet(self, pellet):
		self.food.remove(pellet)
	def draw(self):
		for foodBit in self.food:
			pygame.draw.circle(self.screen, (255,255,255), (foodBit.x,foodBit.y), self.radius)


if __name__ == "__main__":
	print("Test on len 5 @ all angles:\n\n")
	for x in range(360):
		print(str(x)+" deg: "+str(angle2XY(5, x)))
	






