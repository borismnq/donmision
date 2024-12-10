from django.urls import path
from .views import create_organization
from .views import OrganizationsListByAdminView
from .views import OrganizationsListView

urlpatterns = [
    path('create/', create_organization, name='create_organization'),
    path('list-by-admin/', OrganizationsListByAdminView.as_view(), name='list_organizations_by_admin'),
    path('list/', OrganizationsListView.as_view(), name='list_organizations'),
]
