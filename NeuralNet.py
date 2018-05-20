import random

class node:
	value = 0
	weight = 0
	def __init__(self):
		self.weight=random.uniform(-2,2)
	def clear(self):
		self.value=0
	def activate(self):
		return self.value + self.weight;
	def add(self,addAmount):
		self.value+=addAmount
	def setWeight(self,changeAmt):
		self.weight+=changeAmt
	def mutate(self):
		if(random.random()>.5):
			self.weight+=random.uniform(-.5,.5)

class nodeRow:
	row=[]
	def __init__(self,length):
		for i in range(length):
			self.row.append(node())
	def add(self,inputRow):
		for i in range(len(inputRow)-1):
			self.row[i].add(inputRow[i])
	def clear(self):
		for i in range(len(self.row)):
			self.row[i].clear()
	def activate(self):
		outputRow=[]
		for i in range(len(self.row)-1):
			outputRow.append(self.row[i].activate)
	def mutate(self):
		for i in range(len(self.row)-1):
			self.row[i].mutate()
	def getWeight(self,place):
		return self.row[place]
	def getLen(self):
		return len(self.row)
	def combine(self,secondNodeRow):
		newRow=[]
		for i in range(secondNodeRow.getLen()-1):
			if(random.random()>.5):
				newRow.append(self.row[i])
			else:
				newRow.append(secondNodeRow.getWeight(i))
		return newRow

class connectionRow:
	weightList = []
	def __init__(self,length):
		for i in range(length):
			self.weightList.append(random.uniform(-2,2));
	def getWeight(self, position):
		return self.weightList[position]
	def mutate(self):
		for i in range(len(self.weightList)-1):
			if random.random()>.5:
				self.weightList[i]+=random.uniform(-.5,.5)
	def getLen(self):
		return len(self.weightList)
	def combine(self,secondConnection):
		newWeightList=[]
		for i in range(len(self.weightList)-1):
			if random.random()>.5:
				newWeightList.append(self.weightList[i])
			else:
				newWeightList.append(secondConnection.getWeight(i))
		return newWeightList


class net:
	connectors = []
	nodeRows = []
	def __init__(self,layerWidths):
		for i in range(len(layerWidths)-1):
			self.nodeRows.append(nodeRow(layerWidths[i]))
			if i < len(layerWidths)-2:
				tempLayer = []
				for fromNode in range(layerWidths[i]):
					tempLayer.append(connectionRow(layerWidths[i+1]))
				self.connectors.append(tempLayer)
		print(self.nodeRows)
		print("\n\n\n")

	def activate(self, inputRow):
		self.nodeRows[0].add(inputRow)
		currentInput=self.nodeRows[0].activate()
		self.nodeRows[0].clear()
		for nodeLayer in range(len(self.nodeRows)-2):
			tempOutput=[0]*len(self.nodeRows[nodeLayer+1])
			for nodeOutput in currentInput:
				for connectNum in self.connectors[nodeLayer].getLen():
					tempOutput[connectNum]+=nodeOutput*self.connectors.getWeight(connectNum)
			currentInput=self.nodeLayer.activate(tempOutput)
			self.nodeLayer.clear()
		return currentInput

	def mutate(self):
		for i in range(len(self.nodeRows)-1):
			self.nodeRows[i].mutate()
		for i in range(len(self.connectors)-1):
			self.connectors[i].mutate()
	def setConnectors(self,connectionList):
		self.connectors = connectionList
	def setNodeRows(self,nodeRows):
		self.nodeRows = nodeRows
	def getConnectors(self,row):
		return self.connectors[row]
	def getNodeRows(self,nodeRowsNum):
		return self.nodeRows[nodeRowsNum]
	def haveChild(self,secondNet):
		newConnectors=[]
		newNodeRows=[]
		for nodeRow in range(len(self.nodeRows)-1):
			newNodeRows.append(self.nodeRows[nodeRow].combine(secondNet.getNodeRows(nodeRow)))
			# print(self.nodeRows[nodeRow].combine(secondNet.getNodeRows(nodeRow)))
			if nodeRow < len(self.nodeRows)-2:
				for connectNum in range(len(self.connectors[nodeRow])-1):
					newConnectors.append(self.connectors[nodeRow][connectNum].combine(secondNet.getConnectors(nodeRow)[connectNum]))
		print("Child Node Rows")
		print(newNodeRows)
		print('\n\n\n')
		newNet = net([])
		newNet.setConnectors(newConnectors)
		newNet.setNodeRows(newNodeRows)
		return newNet

if __name__ == "__main__":
	print("Running Test of Neural Net")
	testNet = net([2,5,2])
	print("Net Initialized")
	print("Net Output: "+str(testNet.activate([1,0])))
	testNet.mutate()
	print("Mutation Successful")
	print("Mutation Output: "+str(testNet.activate([1,0])))
	secondTestNet = net([2,5,2])
	childNet = testNet.haveChild(secondTestNet)
	print("Child Net Creation Successful")
	print("Child Net Output: "+str(childNet.activate([1,0])))






