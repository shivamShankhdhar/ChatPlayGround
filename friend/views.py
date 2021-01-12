from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import Account

def send_Friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk = user_id)
			try:
				#get any friend requests (active and non-active)
				friend_requests = FriendRequest.objects.filter(sender = user, receiver = receiver)			
				# find if any of them are active
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a friend request.")
						# if non is active, create a friend request
					friend_request = FriendRequest(sender = sender, receiver = receiver)
					friend_request.save()
					payload["response"] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
				
			except FriendRequest.DoesNotExists:
				friend_request = FriendRequest(sender = sender, receiver = receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload["response"] = "Oops! Unable to send friend request"
	else:
		payload["response"] = "Oops! You must be authenticated to send them friend request."
	return HttpResponse(json.dumps(payload), content_type = "application/json")
			
