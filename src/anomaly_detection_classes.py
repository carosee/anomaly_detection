from datetime import datetime
from collections import OrderedDict
import numpy as np
import heapq

# class Purchase:
# 	def __init__(self, timestamp, id, amount):
# 		self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
# 		self.id = id
# 		self.amount = amount

class Social_Network:
	def __init__(self, d, t):
		'''
		Initialize a social network object to check for anomalous purchases.

		d = number of degrees in social network to check
		t = number of purchases to check
		'''
		self.d = d
		self.t = t
		self.id_to_user = {}


	# process individual events streaming in from a json file

	def add_initial_event(self, event_dict):
		'''
		Add an initial event from the input log to this network.

		event: Dictionary representing the parsed json event to add.
		return: None
		'''
		event_type = event_dict['event_type']
		if event_type == 'purchase':
			self.add_purchase(event_dict)
		elif event_type == 'befriend':
			self.add_befriend(event_dict)
		elif event_type == 'unfriend':
			self.add_unfriend(event_dict)
		else:
			print ("ERROR")


	def add_streaming_event(self, event_dict): # t and d not needed as parameters anymore
		'''
		Add in a streaming event from the stream log to this network.
		Check if this event is an anomalous purchase.

		event: Dictionary representing the parsed json event to add.
		return: an OrderedDict representing an anomalous event if an anomaly
		 is detected; boolean False otherwise.
		'''
		event_type = event_dict['event_type']
		if event_type == 'purchase':
			anomaly = self.is_anomaly(event_dict)
			self.add_purchase(event_dict)
			if anomaly: 
				avg, std = anomaly
				new_line = OrderedDict([ ('event_type', 'purchase'),
							('timestamp', event_dict['timestamp']), 
							('id', event_dict['id']), 
							('amount', event_dict['amount']),
							('mean', str('%.2f'%(avg))),
							('sd', str('%.2f'%(std)))
							])
				return new_line
			return False
		elif event_type == 'befriend':
			self.add_befriend(event_dict)
		elif event_type == 'unfriend':
			self.add_unfriend(event_dict)
		else:
			print ("ERROR")


	# fns to update network based on different events

	def add_purchase(self, event_dict):
		'''
		Update network state with purchase event.
		'''
		# update user information
		id = event_dict['id']
		timestamp = event_dict['timestamp']
		amount = event_dict['amount']

		if id in self.id_to_user:
			user = self.id_to_user[id]
			user.purchase(timestamp, amount)
			# update user object
		else:
			new_user = User(id)
			new_user.purchase(timestamp,amount)
			self.id_to_user[id] = new_user
			# create new user object and add to user map
		return (timestamp,amount)


	def add_befriend(self, event_dict):
		'''
		Update network state with befriend event.
		'''
		id1 = event_dict['id1']
		id2 = event_dict['id2']
		if id1 not in self.id_to_user: # user 1 not in user map
			user1 = User(id1)
			self.id_to_user[id1] = user1
		else:
			user1 = self.id_to_user[id1]

		if id2 not in self.id_to_user:
			user2 = User(id2)
			self.id_to_user[id2] = user2
		else:
			user2 = self.id_to_user[id2]

		user1.befriend(id2)
		user2.befriend(id1)
		return user1, user2


	def add_unfriend(self, event_dict):
		'''
		Update network state with unfriend event.
		'''
		id1 = event_dict['id1']
		id2 = event_dict['id2']

		user1 = self.id_to_user[id1]
		user2 = self.id_to_user[id2]
		user1.unfriend(id2)
		user2.unfriend(id1)
		return user1, user2


	# fns to check for anomalies

	def is_anomaly(self, event): # don't need t and d as parameters anymore
		'''
		Check if a given event is anomalous given self.t and self.d.
		An event is anolalous if ...
		Events for which the network has fewer than 2 purchases are not flagged
		 as anomalous.

		event: Dictionary
		return: Tuple of average and std of previous events if the event is
		 anomalous; False if the event is not anomalous.
		'''
		id = event['id']
		amount = float(event['amount'])
		user = self.id_to_user[id]
		friends_list = self.get_friends_list(id)
		purchases = self.get_purchases(friends_list)
		if len(purchases) >= 2:
			amounts = [float(n) for _, _, n in purchases]
			avg = np.mean(amounts)
			std = np.std(amounts)
			cutoff = avg + 3 * std
			if amount > cutoff:
				return (avg, std)
		return False


	def get_friends_list(self, user): # d no longer needed as parameter.
		'''
		Gets the list of all friends in a user's dth degree network, where d is
		 defined by self.d, the degree of the network.
		user: integer id of user to get friends list from.

		return: list of all integer ids of people in user's dth degree network
		'''
		# breadth first search
		count = 0
		friends_list = set()
		queue = [(user, 0)]
		while queue != []:
			# print queue
			curr_user, depth = queue.pop(0)
			if curr_user not in friends_list:
				if depth < self.d+1:
					friends_list.add(curr_user)
					for friend in self.id_to_user[curr_user].friends:
						queue.append((friend,depth+1))
		friends_list.remove(user)
		return friends_list

	def get_purchases(self, friends_list): #no longer need t as parameter
		'''
		Gets the t most recent purchases out of the users in friends_list

		friends_list: a list of integer ids of users in the network.
		return: a list of tuples of (timestamp, amount) for the t most recent
		 purchases in the network.
		'''
		p = []
		for friend in friends_list:
			p.extend(self.id_to_user[friend].purchases)
		return heapq.nlargest(self.t, p)



class User:
	def __init__(self, id):
		self.id = id
		self.friends = set() #id ints
		self.purchases = []

	def befriend(self, user):
		self.friends.add(user)

	def unfriend(self, user):
		self.friends.remove(user)

	def purchase(self, timestamp, amount):
		# new_purchase = Purchase(timestamp, id, amount)
		ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
		ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
		if self.purchases:
			last_purchase = self.purchases[-1]
			last_purchase_ts = last_purchase[0]
			if ts == last_purchase_ts:
				last_purchase_rank = last_purchase[1]
				rank = last_purchase_rank + 1
			else:
				rank = 0
			new_purchase = (ts, rank, amount)
		else:
			new_purchase = (ts, 0, amount)
		self.purchases.append(new_purchase)

		

