import random

class node:
	self.value = 0
	self.weight = 0
	def activate(self):
		return self.value + self.weight;
	def add(self,addAmount):
		self.value+=addAmount
	def changeWeight(self,changeAmt):
		self.weight+=changeAmt

class connections:
	self.weightList = []
	def __init__(self,len):
		for i in range(len):
			self.weightList.append(random.uniform(-1,1));
	def getWeight(self, position):
		return self.weightList[position]
	def mutate(self):
		for i in range(len(self.weightList)):
			self.weightList[i]+=random.uniform(-.5,.5)
	def combine(self,secondConnection):
		newWeightList=[]
		for i in range(len(self.weightList)):
			if(random.random()>.5){
				newWeightList.append(self.weightList[i])
			}else{
				newWeightList.append(secondConnection.getWeight(i))
			}
		return newWeightList





