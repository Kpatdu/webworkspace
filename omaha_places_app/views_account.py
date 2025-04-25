from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth import logout, login

from .mixins import RedirectIfNotAuthenticatedMixin
    

def register_view(request):
    '''
    View to handle user registration.
    '''
    
    if request.user.is_authenticated:
        return redirect("home")  # Redirect if already logged in
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'
            
            return redirect(next_url)
    else:
        form = UserCreationForm()
    
    return render(request, "omaha_places_app/register.html", {
        "form": form,
        "next": request.GET.get('next', '')  # Ensure the next parameter is passed here
    })


def login_view(request):
    '''
    View to handle user login.
    '''

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'

            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, "omaha_places_app/login.html", {
        "form": form,
        "next": request.GET.get('next', '')
        })


def logout_view(request):
    '''
    View to handle user logout.
    '''

    next_url = request.GET.get('next', 'login')
    logout(request)

    return redirect(next_url)


class AccountView(RedirectIfNotAuthenticatedMixin, TemplateView):
    '''
    Class-based view to display user account information.
    '''

    template_name = "omaha_places_app/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        return context
    
    def post(self, request, *args, **kwargs):
        pass