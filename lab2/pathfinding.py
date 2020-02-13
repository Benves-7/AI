
def BreadthFirst(map, width, heigth, start, goal):
	goalIndex = goal
	startIndex = start
	frontier = Queue()
	frontier.put(startIndex)
	came_from = {}
	came_from[startIndex] = True

	while not frontier.empty():
		current = frontier.get()
		for next in MapLoader.getNeighbours(current, map, width, heigth):
			if next not in came_from:
				frontier.put(next)
				came_from[next] = current
		
		if current == goalIndex:
			path = []
			while current != startIndex:
				path.append(current)
				current = came_from[current]
			path.append(startIndex)
			path.reverse()
			return path
	return False

def DepthFirst(map, width, heigth):
	startIndex = GridViewer.getStart(map)
	goalIndex = GridViewer.getGoal(map)
	stack = []
	stack.append(startIndex)
	came_from = {}
	came_from[startIndex] = True

	while len(stack) > 0:
		current = stack.pop()
		for next in GridViewer.getNeighbours(current, map, width, heigth):
			if next not in came_from:
				stack.append(next)
				came_from[next] = current
		
		if current == goalIndex:
			path = []
			while current != startIndex:
				path.append(current)
				current = came_from[current]
			path.append(startIndex)
			path.reverse()
			return path



def AStar(map, width, heigth, window, start, goal = None):
	startIndex = start
	goalIndex = goal
	openNodes = []
	closedNodes = []
	came_from = {}
	came_from[startIndex] = True
	timeBefore = perf_counter()
	noMorePaths = False
	if(goal == None):

		while(1):

			xRand = random.randint(-10, 10)
			yRand = random.randint(-10,10)
			goalIndex = startIndex + (xRand + width * yRand)
			if((goalIndex > 0 and goalIndex < len(map) - 1) and (map[goalIndex].isWalkable) and not (goalIndex == startIndex)):
				if(MapLoader.getDistance(map[startIndex], map[goalIndex]) > 50):
					continue
				#window.drawNode(goalIndex, "red", map)

				break
			if(perf_counter() - timeBefore > 0.001):
				return [startIndex]

	if(perf_counter() - timeBefore > 0.01 or noMorePaths):
		noMorePaths = True
		return [-1]
	openNodes.append(startIndex)
	while len(openNodes) > 0:

		current = MapLoader.getLowestFCost(openNodes, map)
		openNodes.remove(current)
		closedNodes.append(current)
		if(current == goalIndex):
			path = []
			while current != startIndex:
				path.append(current)
				current = came_from[current]
			path.append(startIndex)
			path.pop()
			path.reverse()
			return path

		neighbours = MapLoader.getMoreNeighbours(current, map, width, heigth)
		for node in neighbours:
			if node in closedNodes:
				continue

			costToNeighbor = 0
			if(node == current + 1 or node == current - 1 or node == current + width or node == current - width):
				costToNeighbor = map[current].g_cost + 1
			else:
				costToNeighbor = map[current].g_cost  + 1.4
			
			if(node not in openNodes or costToNeighbor < map[node].g_cost):
				map[node].g_cost = costToNeighbor

				if(node not in openNodes):
					openNodes.append(node)
					map[node].h_cost = MapLoader.getDistance(map[node], map[goalIndex])
				came_from[node] = current
			
			if(perf_counter() - timeBefore > 0.1):
				return [current]

def RandomSearch(map, width, heigth, window):
	startIndex = GridViewer.getStart(map)
	goalIndex = GridViewer.getGoal(map)
	stack = []
	stack.append(startIndex)
	came_from = {}
	came_from[startIndex] = True

	while len(stack) > 0:
		current = stack.pop()
		neighbours = GridViewer.getNeighbours(current, map, width, heigth)
		index = random.randint(0,len(neighbours) - 1)
		stack.append(neighbours[index])
		if(neighbours[index] not in came_from):
			came_from[neighbours[index]] = current
	#	window.drawNode(current, "green", map)
		if current == goalIndex:
			path = []
			while current != startIndex:
				path.append(current)
				current = came_from[current]
			path.append(startIndex)
			path.reverse()
			return path
		
from queue import Queue
from maploader import *
import random
from time import perf_counter