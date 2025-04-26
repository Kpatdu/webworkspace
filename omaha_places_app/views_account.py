from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.views.generic import TemplateView
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .mixins import RedirectIfNotAuthenticatedMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import SavedLocation
from django.contrib import messages

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

@login_required
def reset_password_view(request):
    '''
    View to handle password reset.
    '''

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("account")  # Redirect to account page after password reset
        else:
            return render(request, "omaha_places_app/change_password.html", {
                "form": form
            })
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "omaha_places_app/change_password.html", {
        "form": form
    })

class AccountView(RedirectIfNotAuthenticatedMixin, TemplateView):
    '''
    Class-based view to display user account information.
    '''

    template_name = "omaha_places_app/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        return context

@login_required
def save_location(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Save the data to the SavedRestaurant model
        SavedLocation.objects.create(name=name, description=description)
        messages.success(request, f"Location '{name}' has been saved successfully!")

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the same page

@login_required
def delete_saved_location(request, location_id):
    if request.method == "POST":
        saved_location = get_object_or_404(SavedLocation, id=location_id)
        saved_location.delete()
        messages.success(request, f"Location '{saved_location.name}' has been deleted successfully!")   
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def save_location_view(request):
    saved_locations = SavedLocation.objects.all()
    return render(request, "omaha_places_app/saved_locations.html",
                  {'saved_locations': saved_locations})