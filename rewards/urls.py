from django.urls import path

from .views import create_reward
from .views import RewardListByOrganizationView
urlpatterns = [
    path('create/', create_reward, name='create_reward'),
    path('list-by-organization/<int:organization_id>', RewardListByOrganizationView.as_view(), name='list_rewards_by_organization'),
]
