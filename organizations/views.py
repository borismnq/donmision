from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Organization
# Create your views here.
from django.views.generic import FormView, TemplateView




@login_required
@permission_required(["is_admin"])
def organization_detail(request, organization_id):
    request.GET.get('organization')
    context = {}
    # context["errors"] = []
    context["organization_id"] = organization_id
    # # context["messages"] = {}
    # if request.method=="POST":
    #     if not request.user:
    #         context["errors"].append("User is required")
    #     if not request.user.is_authenticated:
    #         context["errors"].append("Login is required")
    #     name = request.POST.get("name")
    #     description = request.POST.get("description")
    #     if not name:
    #         context["errors"].append("Name is required")
    #     if not context["errors"]:
    #         Organization.objects.create(
    #             name=name,
    #             description=description,
    #             created_by=request.user
    #         )
    #         context["success"] = True
    #         context["success_message"] = f"Organization '{name}' created!"
    #         return redirect('list_organizations_by_admin')
    # else:
    #     print(request.method)
    #     print(request)
    return render(request, 'missions/list_missions_by_organization.html',context=context)


@login_required
@permission_required(["is_admin"])
def create_organization(request):
    context = {}
    context["errors"] = []
    context["success"] = False
    # context["messages"] = {}
    if request.method=="POST":
        if not request.user:
            context["errors"].append("User is required")
        if not request.user.is_authenticated:
            context["errors"].append("Login is required")
        name = request.POST.get("name")
        description = request.POST.get("description")
        if not name:
            context["errors"].append("Name is required")
        if not context["errors"]:
            Organization.objects.create(
                name=name,
                description=description,
                created_by=request.user
            )
            context["success"] = True
            context["success_message"] = f"Organization '{name}' created!"
            return redirect('list_organizations_by_admin')
    else:
        print(request.method)
        print(request)
    return render(request, 'organizations/create_organization.html',context=context)

class OrganizationsListView(LoginRequiredMixin, TemplateView):
    template_name = "organizations/list_organizations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = Organization.objects.filter(
            status='active'
        ).order_by('name').all()
        return context

class OrganizationsListByAdminView(PermissionRequiredMixin, TemplateView):
    template_name = "organizations/list_organizations.html"
    permission_required = "is_admin"

    def get_context_data(self, **kwargs):
        print("org view")
        context = super().get_context_data(**kwargs)
        context["organizations"] = Organization.objects.filter(
            created_by=self.request.user,
            status='active',
        ).order_by('name').all()
        self.request.session["organization_id"] = None
        return context
    