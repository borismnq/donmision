from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Reward
from organizations.models import Organization
# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, TemplateView

@login_required
@permission_required(["is_admin"])
def create_reward(request):
    context = {}
    context["errors"] = []
    context["success"] = False
    organization_id = request.session.get("organization_id")
    print(f"{organization_id=}")
    if not organization_id:
        return redirect('list_organizations_by_admin')
    organization = Organization.objects.filter(
        id=organization_id,
        status='active'
    ).first()
    if not organization:
        context["errors"].append("Organization not found")
        return redirect('list_organizations_by_admin')
    if request.method=="POST":
        if not request.user:
            context["errors"].append("User is required")
        if not request.user.is_authenticated:
            context["errors"].append("Login is required")
        title = request.POST.get("title")
        description = request.POST.get("description")
        if not title:
            context["errors"].append("Title is required")
        if not context["errors"]:
            
            new_reward = Reward(
                organization=organization,
                title=title,
                description=description,
            )
            print(f"{new_reward=}")
            new_reward.save()
            context["success"] = True
            context["success_message"] = f"Reward '{title}' created!"
            return redirect('list_rewards_by_organization', organization_id=organization_id)
    return render(request, 'rewards/create_reward.html',context=context)

class RewardListByOrganizationView(PermissionRequiredMixin, TemplateView):
    template_name = "rewards/list_rewards_by_organization.html"
    permission_required = "is_admin"

    # def 
    def get_context_data(self, **kwargs):
        print("rewards view")

        context = super().get_context_data(**kwargs)
        print(f"{context=}")
        context["errors"] = []
        organization_id = context.get('organization_id')
        self.request.session["organization_id"] = organization_id
        print(f"{self.request.session.get("organization_id")=}")
        if not organization_id:
            context["errors"].append("Not organization id provided")
            return context
        organization = Organization.objects.filter(id=organization_id).first()
        if not organization:
            context["errors"].append("Organization not found")
            return context
        context["rewards"] = Reward.objects.filter(
            status="active",
            organization=organization,
        ).order_by('title').all()
        context["organization"] = organization
        return context
 