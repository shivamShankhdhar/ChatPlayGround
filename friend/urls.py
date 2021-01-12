from django.urls import path

from .views import (
	send_Friend_request,
)

app_name = "friend"

urlpatterns = [
	path("friend_request/", send_Friend_request, name ="friend-request"),
]