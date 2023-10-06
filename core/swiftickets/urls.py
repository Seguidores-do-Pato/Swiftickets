from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('logout/',views.logoutUser, name="logout"),
]