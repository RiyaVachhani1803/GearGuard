from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("requests/", views.request_list, name="request_list"),
    path("equipment/", views.equipment_list, name="equipment_list"),
    path("equipment/<int:pk>/", views.equipment_requests, name="equipment_requests"),
    path("requests/<int:pk>/status/<str:status>/", views.update_status, name="update_status"),
    path("requests/new/", views.create_request, name="create_request"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("equipment/new/", views.create_equipment, name="create_equipment"),


]
