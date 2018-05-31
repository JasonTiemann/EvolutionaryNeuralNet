import pygame
import AgentClasses
import NeuralNet
import math
import time
from random import randint

def pointDist(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

pygame.init()

displayScreen = pygame.display.set_mode((500,500))
displayScreen.fill((0,0,0))

running = True

topNet = NeuralNet.net([2,10,4])
winNet = NeuralNet.net([2,10,4])
topScore = 0
generation = 0

while running:
	generation+=1
	print(generation)
	print("TopScore: "+str(topScore))
	agentOption = randint(0,5)
	# 2 inputs: see food and see wall
	# 4 outputs: left, right, forwards, and back
	agent1Net = winNet
	if agentOption == 0:
		agent2Net = NeuralNet.net([2,10,4])
	elif agentOption == 1:
		agent2Net = winNet.mutate()
	elif agentOption == 2:
		agent2Net = topNet.mutate()
	elif agentOption == 3:
		agent2Net = topNet.haveChild(winNet)
	elif agentOption == 4:
		agent2Net = topNet.haveChild(NeuralNet.net([2,10,4]))
	elif agentOption == 5:
		agent2Net = winNet.haveChild(NeuralNet.net([2,10,4]))

	agent1 = AgentClasses.Agent(displayScreen,pos=[200,255])
	agent2 = AgentClasses.Agent(displayScreen,pos=[300,255])
	food = AgentClasses.foodPellets(displayScreen)
	agent1Score = 0
	agent2Score = 0
	startTime = time.time()
	while True:
		for pellet in food.food:
			if pointDist(agent1.pos[0],agent1.pos[1],pellet.x,pellet.y) < agent1.radius:
				agent1Score+=1
				food.eatPellet(pellet)
			elif pointDist(agent2.pos[0],agent2.pos[1],pellet.x,pellet.y) < agent2.radius:
				agent2Score+=1
				food.eatPellet(pellet)


		agent1Food = agent1.seeFood(food)
		agent2Food = agent2.seeFood(food)
		agent1Wall = agent1.seeWall()
		agent2Wall = agent2.seeWall()

		agent1Move = agent1Net.activate([agent1Food,agent1Wall])
		agent2Move = agent2Net.activate([agent2Food,agent2Wall])



		if round(agent1Move[0]) >= 1:
			agent1.rotate("right")
		if round(agent1Move[1]) >= 1:
			agent1.rotate("left")
		if round(agent1Move[2]) >= 1:
			agent1.move("forward")
		if round(agent1Move[3]) >= 1:
			agent1.move("back")

		if round(agent2Move[0]) >= 1:
			agent2.rotate("right")
		if round(agent2Move[1]) >= 1:
			agent2.rotate("left")
		if round(agent2Move[2]) >= 1:
			agent2.move("forward")
		if round(agent2Move[3]) >= 1:
			agent2.move("back")

		#exit reasons (speeds up process)
		gameOver=False
		if time.time() - startTime >= 10:
			if agent1Score >= agent2Score:
				winNet = agent1Net
			else:
				winNet = agent2Net
			gameOver=True
		#If agent is just spinning
		if time.time() - startTime >= 2:
			if agent1.pos == [200,250]:
				gameOver=True
			if agent1.pos == [300,250]:
				gameOver=True
			
		#If agent does not respond to stimuli
		elif round(agent1Move[0]) == round(agent1Move[1]) and round(agent1Move[2]) == round(agent1Move[3]):
			gameOver=True
		elif round(agent2Move[0]) == round(agent2Move[1]) and round(agent2Move[2]) == round(agent2Move[3]):
			gameOver=True
		#If agent out of bounds
		elif agent1.pos[0] > 500 or agent1.pos[0] < 0 or agent1.pos[1] > 500 or agent1.pos[1] < 0:
			gameOver=True
		elif agent2.pos[0] > 500 or agent2.pos[0] < 0 or agent2.pos[1] > 500 or agent2.pos[1] < 0:
			gameOver=True

		if gameOver:
			if agent1Score >= agent2Score:
				winNet = agent1Net
			else:
				winNet = agent2Net
			if agent1Score > topScore:
				print("Topnet Change to 1")
				topScore=agent1Score
				topNet = agent1Net
			if agent2Score > topScore:
				print("Topnet Change to 2")
				topScore=agent2Score
				topNet = agent2Net
			break

		displayScreen.fill((0,0,0))
		food.draw()
		agent1.draw()
		agent2.draw()
		pygame.event.pump()
		pygame.display.update()




		#If user clicks x on window, quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

