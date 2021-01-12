from django.db import models

from django.conf import settings
from django.utils import timezone

class FriendList(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends 	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name="friend")

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add account

		"""
		if not account in self.friends.all():
			self.friends.add(account)
			# self.save()

	def remove_friend(self, account):
		"""
		Remove friend

		"""
		if account in self.friends.all():
			self.friends.remove(account)
			# self.save()

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.

		"""
		
		"""
			both of the wil not be friend if 
			someone remove from friend list so
			remove from both of the friend lists
			both cases written below 

		"""
		remover_friends_list = self #person terminating the friendship
		
		remover_friends_list.remove_friend(removee)
		
		
		# remove friend from removee friend list 
		friends_list = FriendList.objects.get(user = removee) 			# get the romovee
		friends_list.remove_friend(self.user)


	def is_mutual_friend(self, friend):
		"""
		is this a  friend ?

		"""
		if friend in self.friends.all():
			return True
		return False

# friend request model 
class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. Semder:
			-Person sending /Initiating the friend request
		2. Reciever:
			-Person receiving the friend request
	"""
	sender 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "sender")
	receiver 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "receiver")
	is_active 		= models.BooleanField(blank = True, null = False, default = True)
	timestamp 		= models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.sender.username

	# accept friend request
	def accept(self):
		"""
		Accept a friend request
		Update both friend list 

		"""
		receiver_friend_list = FriendList.get(user=self.receiver)
		if receiver_friend_list :
			sender_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user = self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		"""
		Decline a friend request
		it is "declined " by setting the "is_active" field to false

		"""
		self.is_active = False
		self.save()

	def cancel(self):
		"""
		cancel a friend request 
		it is 'cancelled' by setting the 'is_active' field to False
		it executed from the sender's End

		"""
		self.is_active = False
		self.save()





	 