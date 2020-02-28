from queue import Queue

def breadthFirst(mapHandle, start, goal):
	goalIndex = goal.ID
	startIndex = start.ID
	frontier = Queue()
	frontier.put(startIndex)
	came_from = {}
	came_from[startIndex] = True

	while not frontier.empty():
		current = frontier.get()
		for next in mapHandle.getNeighbours(current):
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

def breadthFirstW(mapHandle, start, goal):
	goalIndex = goal.tileId
	startIndex = start.tileId
	frontier = Queue()
	frontier.put(startIndex)
	came_from = {}
	came_from[startIndex] = True

	while not frontier.empty():
		current = frontier.get()
		for next in mapHandle.getNeighboursW(current):
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