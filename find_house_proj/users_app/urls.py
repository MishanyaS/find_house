from django.urls import path
from users_app.views import CustomUserRegistrationView, CustomUserLoginView, ProfileDetailView, CustomUserDeleteView, CustomUserUpdateView
from django.contrib.auth.views import LogoutView

app_name = 'users_app'

urlpatterns = [
    # Register and Login URLs
    path('register/', CustomUserRegistrationView.as_view(), name='registration'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile URLs
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_read'),
    path('user/edit/<int:pk>/', CustomUserUpdateView.as_view(), name='user_settings_update'),
    path('user/delete/<int:pk>/', CustomUserDeleteView.as_view(), name='user_delete'),
]
