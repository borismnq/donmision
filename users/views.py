from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .admin import UserCreationForm
# from 

# Create your views here.
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

@login_required
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST)
    context = {}
    if request.method=="POST":
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data.get('email')
            form.save()
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password1)
            login(request, user)
            return redirect('home')
        else:
            context["errors"] = [error for _, error in form.errors.as_data().items()]
    context["form"] = form
    return render(request, 'users/register.html', context)

def login_view(request):
    context = {}
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            context["error"]= "Invalid email or password"
        else:
            login(request, user)
            return redirect('home')
    if request.method=="GET":
        if request.user.is_authenticated:
            return redirect('home')
    return render(request, 'users/login.html',context)

