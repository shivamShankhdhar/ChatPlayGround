from django.urls import path
from .views import (
    account_view,
    edit_account_view,
    crop_image
)

app_name = "accounts"

urlpatterns = [
    path('<user_id>/', account_view, name='view'),
    path('<user_id>/edit/', edit_account_view, name='edit'),
    path('<user_id>/edit/crop-image/', crop_image, name='crop_image'),
]