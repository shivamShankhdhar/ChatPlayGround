from django.urls import path
from .views import (
    account_view,
)

app_name = "accounts"

urlpatterns = [
    path('<user_id>/', account_view, name='view')
]