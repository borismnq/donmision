from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Mission
from organizations.models import Organization
from rewards.models import Reward
# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, TemplateView

@login_required
@permission_required(["is_admin"])
def create_mission(request):
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
    create_mission_step = request.session.get("create_mission_step")
    if not create_mission_step:
        print("NOT CREATION MISSION")
        request.session["create_mission_step"] = 1
    print(f"{request.session.get('create_mission_step')=}")
    if request.method=="POST":
        if not request.user:
            context["errors"].append("User is required")
        if not request.user.is_authenticated:
            context["errors"].append("Login is required")
        # organization = request.POST.get("organization")
        
        if not organization_id:
            context["errors"].append("Organization is required")
        
            # context["current_step"] = 1

        if request.session.get("create_mission_step") == 1:

            # title = request.POST.get("title")
            # description = request.POST.get("description")
            # start_date = request.POST.get("start-date")
            # end_date = request.POST.get("end-date")
            request.session["mission_title"] = request.POST.get("title")
            request.session["mission_description"] = request.POST.get("description")
            request.session["mission_start_date"] = request.POST.get("start-date")
            request.session["mission_end_date"] = request.POST.get("end-date")
            print(organization_id)
            print(request.session["mission_title"])
            print(request.session["mission_description"])
            print(request.session["mission_start_date"])
            print(request.session["mission_end_date"])
            if not request.session["mission_title"]:
                context["errors"].append("Title is required")
            if not request.session["mission_start_date"]:
                context["errors"].append("Start date is required")
            if not request.session["mission_end_date"]:
                context["errors"].append("End date is required")
            if not context["errors"]:
                print("==========BEFORE CREATE MISSION===========")
                print(organization_id)
                # Mission.objects.create(
                #     organization_id=organization_id,
                #     title=title,
                #     description=description,
                #     start_date=start_date,
                #     end_date=end_date,
                # )
                
                # new_mission = Mission(
                #     organization=organization,
                #     title=title,
                #     description=description,
                #     start_date=start_date,
                #     end_date=end_date,
                # )
                # print(f"{new_mission=}")
                # new_mission.save()
                # context["next_step"] = True
                context["create_mission_step"] = request.session["create_mission_step"] = 2
                # context["success_message"] = f"Mission '{title}' created!"
                # return "YES"
                # return redirect(f'list_missions_by_organization/{organization_id}')
                # return redirect('list_missions_by_organization', organization_id=organization_id)
                print(f"{request.session["create_mission_step"]=}")
                return render(request, 'missions/create_mission.html',context=context)
        elif request.session.get("create_mission_step") == 2:
            
            return render(request, 'missions/create_mission.html',context=context)
    # else:
    #     print(request.method)
    #     print(request)
    print(f"{request.method=}")
    print(f"{context=}")
    context["create_mission_step"] = request.session.get("create_mission_step")
    if request.session.get("create_mission_step") == 2:
        print("=STEP2 GET=")
        rewards_list = Reward.objects.filter(organization__id=organization_id).all()
        context["rewards_list"] = rewards_list
        context["selected_rewards_list"] = rewards_list
        print(f"{context=}")

    print(f"{context=}")
    return render(request, 'missions/create_mission.html',context=context)

class MissionListByOrganizationView(PermissionRequiredMixin, TemplateView):
    template_name = "missions/list_missions_by_organization.html"
    permission_required = "is_admin"

    # def 
    def get_context_data(self, **kwargs):
        print("missions view")

        context = super().get_context_data(**kwargs)
        print(f"{context=}")
        context["errors"] = []
        organization_id = context.get('organization_id')
        print("=================AAAAAAAA=============")
        print(f"{organization_id=}")
        print(f"{self.request.session.get("organization_id")=}")
        # if not self.request.session.get("organization_id"):
        #     print("==========SET ORGANIZATION SESSION DAT===========")
        self.request.session["organization_id"] = organization_id
        print(f"{self.request.session.get("organization_id")=}")
        if not organization_id:
            context["errors"].append("Not organization id provided")
            return context
        organization = Organization.objects.filter(id=organization_id).first()
        if not organization:
            context["errors"].append("Organization not found")
            # print()
            return context
        context["missions"] = Mission.objects.filter(
            ~Q(status__in=[
                'cancelled'
                'inactive'
                'deleted'
            ]),
            organization=organization,
        ).order_by('title').all()
        context["organization"] = organization
        return context
    