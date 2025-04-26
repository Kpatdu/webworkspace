from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import SavedLocation, Profile
from .mixins import RedirectIfNotAuthenticatedMixin


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'home'

            return redirect(next_url)
    else:
        form = UserCreationForm()
    
    return render(request, "omaha_places_app/register.html", {
        "form": form,
        "next": request.GET.get('next', '')
    })

def login_view(request):
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
    next_url = request.GET.get('next', 'login')
    logout(request)
    return redirect(next_url)


class AccountView(RedirectIfNotAuthenticatedMixin, TemplateView):
    '''
    Class-based view to handle user account page.
    '''

    template_name = "omaha_places_app/account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        return context
    

class ResetPasswordView(RedirectIfNotAuthenticatedMixin, View):
    '''
    Class to handle resetting a user's password.
    '''

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "omaha_places_app/change_password.html", {"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True})  # JSON response
            return redirect("account")
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Instead of returning a whole HTML form, send errors back in JSON
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "errors": errors}, status=400)
        
        return render(request, "omaha_places_app/change_password.html", {"form": form})
    

class SaveLocationView(RedirectIfNotAuthenticatedMixin, View):
    '''
    Class to handle saving a location to the user's saved locations.
    '''

    def post(self, request):
        location_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        # If user is not authenticated, save info in session and redirect to login
        if not request.user.is_authenticated:
            request.session['pending_save_location'] = {
                'id': location_id,
                'name': name,
                'description': description,
            }
            return redirect(f"{reverse('login')}?next={request.path}")

        return self.save_location(request, location_id, name, description)

    def save_location(self, request, location_id, name, description):
        location_type = request.POST.get('location_type')

        saved_location = SavedLocation.objects.filter(user=request.user, location_id=location_id).first()

        if saved_location:
            messages.info(request, f"You have already saved '{name}'.")
        else:
            SavedLocation.objects.create(
                user=request.user,
                location_id=location_id,
                name=name,
                description=description,
                location_type=location_type
            )
            messages.success(request, f"Location '{name}' has been saved successfully!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeleteSavedLocationView(RedirectIfNotAuthenticatedMixin, View):
    '''
    Class to handle deleting a saved location from the user's saved locations.
    '''

    def post(self, request, location_id):
        saved_location = get_object_or_404(SavedLocation, id=location_id, user=request.user)
        saved_location.delete()
        messages.success(request, f"Location '{saved_location.name}' has been deleted successfully!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class SavedLocationListView(RedirectIfNotAuthenticatedMixin, ListView):
    '''
    Class to handle displaying a list of the user's saved locations.
    '''
    
    model = SavedLocation
    template_name = "omaha_places_app/saved_locations.html"
    context_object_name = 'saved_locations'

    def get_queryset(self):
        return SavedLocation.objects.filter(user=self.request.user)
    

class UpdateProfilePictureView(RedirectIfNotAuthenticatedMixin, View):
    '''
    Allows a user to update their profile picture to one of the preset options.
    '''

    def post(self, request):
        selected_picture = request.POST.get('profile_picture')

        if selected_picture and selected_picture.startswith('profile_pictures/profile'):
            profile, created = Profile.objects.get_or_create(user=request.user)

            profile.profile_picture = selected_picture
            profile.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Invalid profile picture selection.')

        return redirect('account')

