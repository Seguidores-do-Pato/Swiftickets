from django.contrib import admin

# Register your models here.
from .models import User, Ticket, Purchase, Event

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Purchase)
admin.site.register(Event)
