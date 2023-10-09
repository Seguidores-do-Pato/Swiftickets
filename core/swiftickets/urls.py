from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    path('login/',views.loginUser, name="login"),
    path('owner/',views.ownerEvents, name="ownerEvents"),
    path('event/create/', views.eventCreate, name='eventCreate'),
    path('event', views.eventViewer, name='eventViewer'),
    path('event/purchase/', views.purchaseTicket, name='purchaseTicket'),
    path('tickets/',views.ownerTicket, name="ownerTicket"),
    path('edit_ticket/<int:pk>/', views.editTicket, name='edit_ticket'),
    path('suporte/',views.editTicket, name="maxEdit"),
]