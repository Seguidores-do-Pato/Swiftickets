from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    path('login/',views.loginUser, name="login"),
]