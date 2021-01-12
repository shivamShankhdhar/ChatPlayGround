from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# auth views 
from django.contrib.auth import views as auth_views

from personal.views import (
    home_screen_view
)

from accounts.views import (
    register_view,
    login_view,
    logout_view,
    account_search_view
)


urlpatterns = [
    path('', home_screen_view, name = 'home'),
    path('accounts/', include('accounts.urls', namespace = 'accounts')),
    path('admin/', admin.site.urls),
    path('friend/', include('friend.urls', namespace = 'friend')),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('register/', register_view, name = 'register'),
    path('search/', account_search_view, name = 'search'),

    # Password reset links 
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)








  