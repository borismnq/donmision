from django.urls import path

from .views import create_mission
from .views import MissionListByOrganizationView
urlpatterns = [
    path('create/', create_mission, name='create_mission'),
    path('list-by-organization/<int:organization_id>', MissionListByOrganizationView.as_view(), name='list_missions_by_organization'),
]
