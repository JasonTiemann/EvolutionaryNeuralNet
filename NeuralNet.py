import random

class node:
	
	def __init__(self):
		self.value = 0
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
	def __init__(self,length):
		self.row=[]
		for i in range(length):
			self.row.append(node())
	def add(self,inputRow):
		for i in range(len(self.row)):
			self.row[i].add(inputRow[i])
	def clear(self):
		for i in range(len(self.row)):
			self.row[i].clear()
	def activate(self):
		outputRow=[]
		for i in range(len(self.row)):
			outputRow.append(self.row[i].activate())
		return outputRow
	def mutate(self):
		for i in range(len(self.row)):
			self.row[i].mutate()
	def setWeight(self,rowWeight):
		self.row = rowWeight
	def getAllWeight(self):
		return self.row
	def getWeight(self,place):
		return self.row[place]
	def getLen(self):
		return len(self.row)
	def combine(self,secondNodeRow):
		newRow=[]
		for i in range(secondNodeRow.getLen()):
			if(random.random()>.5):
				newRow.append(self.row[i])
			else:
				newRow.append(secondNodeRow.getWeight(i))
		outRow = nodeRow(0)
		outRow.setWeight(newRow)
		return outRow

class connectionRow:
	def __init__(self,length):
		self.weightList = []
		for i in range(length):
			self.weightList.append(random.uniform(-2,2));
	def getWeight(self, position):
		return self.weightList[position]
	def setWeight(self, newWeightList):
		self.weightList=newWeightList
	def mutate(self):
		for i in range(len(self.weightList)):
			if random.random()>.5:
				self.weightList[i]+=random.uniform(-.5,.5)
	def getLen(self):
		return len(self.weightList)
	def combine(self,secondConnection):
		newWeightList=[]
		for i in range(len(self.weightList)):
			if random.random()>.5:
				newWeightList.append(self.weightList[i])
			else:
				newWeightList.append(secondConnection.getWeight(i))
		newConnection = connectionRow(0)
		newConnection.setWeight(newWeightList)
		return newConnection


class net:
	def __init__(self,layerWidths):
		self.connectors = []
		self.nodeRows = []
		for i in range(len(layerWidths)):
			self.nodeRows.append(nodeRow(layerWidths[i]))
			if i < len(layerWidths)-1:
				tempLayer = []
				for fromNode in range(layerWidths[i]):
					tempLayer.append(connectionRow(layerWidths[i+1]))
				self.connectors.append(tempLayer)

	def activate(self, inputRow):
		self.nodeRows[0].add(inputRow)
		currentInput=self.nodeRows[0].activate()
		self.nodeRows[0].clear()
		for nodeLayer in range(len(self.nodeRows)-1):
			for node in range(len(currentInput)):
				tempOutput=[]
				for connectNum in range(self.connectors[nodeLayer][0].getLen()):
					tempOutput.append(currentInput[node]*self.connectors[nodeLayer][node].getWeight(connectNum))
				self.nodeRows[nodeLayer+1].add(tempOutput)
			currentInput=self.nodeRows[nodeLayer].activate()
			self.nodeRows[node].clear()
		return currentInput

	def mutate(self):
		for i in range(len(self.nodeRows)):
			self.nodeRows[i].mutate()
		for fromConnect in range(len(self.connectors)):
			for toConnect in range(len(self.connectors[fromConnect])):
				self.connectors[fromConnect][toConnect].mutate()
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
		for nodeRow in range(len(self.nodeRows)):
			newNodeRows.append(self.nodeRows[nodeRow].combine(secondNet.getNodeRows(nodeRow)))
			if nodeRow < len(self.nodeRows)-1:
				tempConnectionRow=[]
				for connectNum in range(len(self.connectors[nodeRow])):
					tempConnectionRow.append(self.connectors[nodeRow][connectNum].combine(secondNet.getConnectors(nodeRow)[connectNum]))
			newConnectors.append(tempConnectionRow)
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






