from config import *
from managers import *
from threading import *
from time import sleep, perf_counter

FRAMES		= 30
FPS_LIMIT	= 1/FRAMES

def managers():
	print("managers thread started.")
	while True:
		start = perf_counter()
		ResourceManager.update()
		BuildingManager.update()
		time = perf_counter() - start
		if time < FPS_LIMIT:
			sleep(FPS_LIMIT - time)
		else:
			print("Manager updates takes to much time..")

def units():
	print("unit thread started.")
	while True:
		start = perf_counter()
		UnitManager.update()
		time = perf_counter() - start
		if time < FPS_LIMIT:
			sleep(FPS_LIMIT - time)
		else:
			print("Unit update takes to much time..")

if __name__ == '__main__':

	runSetup()

	Thread(target= managers).start()
	Thread(target= units).start()

	while True:
		start = perf_counter()
		WindowManager.update(FPS_LIMIT)
		time = perf_counter() - start
		if time < FPS_LIMIT:
			sleep(FPS_LIMIT - time)
		else:
			print("Window update takes to much time..")
			
		

