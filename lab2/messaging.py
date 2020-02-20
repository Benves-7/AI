from timeManager import *
import random

class MessageDispatcher:
	delayedMessages = []

	def sendMessage(sender, reciever, message, delay, time, place, type):#Type 1: request, Type 2: ack, Type 3: go now, Type 4: leave
		header = {'sender': sender, 'reciever': reciever, 'message': message,'delay': delay, 'time': time, 'place': place, 'type': type}

		if(int(delay) > 0):
			timeToSend = TimeManager.currentTick + delay
			header['delay'] = timeToSend
			MessageDispatcher.delayedMessages.append(header)
			return 0
		EntityManager.getEntity(reciever).recvMessage(header)

	#Send the delayed message if enough time has passed
	def dispatchDelayed():
		for message in MessageDispatcher.delayedMessages:
			if(message['delay'] == TimeManager.currentTick):
				MessageDispatcher.sendMessage(message['sender'], message['reciever'], message['message'],0 , message['time'], message['place'], 3)
				#MessageDispatcher.delayedMessages.remove(message)

