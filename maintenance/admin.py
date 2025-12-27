from django.contrib import admin
from .models import Team, Equipment, MaintenanceRequest

admin.site.register(Team)
admin.site.register(Equipment)
admin.site.register(MaintenanceRequest)
