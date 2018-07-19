from django.urls import path
from . import views

app_name = 'prof'
urlpatterns = [
    path ('profileInfo/', views.profileInfo, name = 'profileInfo'),
    path('register/', views.RegistrationView, name = 'register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('add_reserved_card/', views.add_reserved_card, name = "add_reserved_card"),
    path('add_preferred_card/', views.add_preferred_card, name = "add_preferred_card"),
]