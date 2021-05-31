# -*- coding: utf-8 -*-
"""
Created on Sun May 30 07:32:27 2021

@author: Harivyas
"""

class Node:

	def __init__(self,name,price,cpus):
		self.name=name
		self.price=price
		self.cpus=cpus
		self.nextNode=self
		self.multiplier=1
		self.count=0

def initialProcess(nodeList):
	for i in range(1,len(nodeList)):
		multiply = nodeList[i].cpus//nodeList[i-1].cpus
		result = multiply*nodeList[i-1].price
		if nodeList[i].price > result:
			nodeList[i].price = multiply*nodeList[i-1].price
			nodeList[i].nextNode = nodeList[i-1].nextNode
			nodeList[i].multiplier = multiply*nodeList[i-1].multiplier

def findCostForcpus(nodeList,total_cpus):
	nn = len(nodeList)-1
	while total_cpus > 0 and nn >=0:
		if total_cpus >= nodeList[nn].cpus:
			total_cpus = total_cpus - nodeList[nn].cpus
			nodeList[nn].nextNode.count = nodeList[nn].nextNode.count + nodeList[nn].multiplier
		else:
			nn = nn-1
	if total_cpus > 0:  #if total_cpus is less than minimum core available
		total_cpus = total_cpus - nodeList[0].cpus
		nodeList[0].nextNode.count = nodeList[0].nextNode.count + nodeList[0].multiplier

def findcpusForCost(nodeList,total_cost):
	nn = len(nodeList)-1
	while total_cost > 0 and nn >=0 :
		if total_cost >= nodeList[nn].price:
			total_cost = total_cost - nodeList[nn].price
			nodeList[nn].nextNode.count = nodeList[nn].nextNode.count + nodeList[nn].multiplier
		else:
			nn = nn-1    	                

def parseDict(instances,server_name):
        server = instances[server_name]
        nodeList = []
        mul = 1
        for j in ('large','xlarge','2xlarge','4xlarge','8xlarge','10xlarge'):
                result = server.get(j,-1)
                if result != -1:
                        node = Node(j,result,mul)
                        nodeList.append(node)
                mul = mul * 2
        return nodeList

def multiplyCost(nodeList,hours):
	for node in nodeList:
		node.price = float(node.price * hours)

def findTotalCost(nodeList):
	totalCost=0
	for node in nodeList:
		if node.count > 0:
			totalCost = totalCost + (node.price * node.count)
	return totalCost	
	
def get_costs(instances,hours,cpus,price):
	allNodes = []
	for server in instances:
		nodeList = parseDict(instances,server)
		initialProcess(nodeList)
		if cpus != 0 and price == 0.0:
			multiplyCost(nodeList,hours)
			findCostForcpus(nodeList,cpus)
			totalCost=findTotalCost(nodeList)
		elif cpus == 0 and price != 0.0:
			multiplyCost(nodeList,hours)
			findcpusForCost(nodeList,price)
			totalCost=findTotalCost(nodeList)
		elif cpus !=0 and price !=0.0:
			multiplyCost(nodeList,hours)
			findCostForcpus(nodeList,cpus)
			totalCost=findTotalCost(nodeList) 
			if totalCost>price:
				continue
		else:
			continue  	
		newNode = {}	
		newNode["region"]=server
		newNode["total_cost"]="$"+"{0:.2f}".format(totalCost)
		newNode["servers"] = []
		for node in nodeList:
			if node.count > 0:
				tup = node.name, node.count
				newNode["servers"].append(tup)
		allNodes.append(newNode)
		allNodes.sort(key=lambda x: x["total_cost"])
	print (allNodes)

if __name__ == "__main__":
	instances={'us-east': 
		   {'large': 0.12,
		    'xlarge': 0.23,
		    '2xlarge': 0.45,
		    '4xlarge': 0.774,
		    '8xlarge': 1.4,
		    '10xlarge': 2.82
		   },
                    'us-west': 
		   {
		    'large': 0.14,
		    '2xlarge': 0.413,
		    '4xlarge': 0.89,
	            '8xlarge': 1.3,
		    '10xlarge': 2.97
		   }
		  }
	hours = input("Hours:")
	cpus = input("Cpus:")
	price = float(input("Price:"))
	get_costs(instances,hours,cpus,price)
