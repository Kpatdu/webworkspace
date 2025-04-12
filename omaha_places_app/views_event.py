import calendar
from datetime import datetime, timedelta, date

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Restaurant, Place, Event
from .forms import EventForm
from .utils import Calendar
from .mixins import RedirectIfNotAuthenticatedMixin

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.auth.views import reverse_lazy 
from django.utils.safestring import mark_safe
    

class CalendarView(RedirectIfNotAuthenticatedMixin, ListView):
    '''
    Class-based view to render the home page.
    Ensures users only see their own events.
    Requires user to be authenticated.
    '''

    model = Event
    template_name = 'omaha_places_app/calendar.html'
    success_url = reverse_lazy('calendar')


    def get_date(self, req_day): # req_day = requested year and month
        '''
        Function to get the date.
        '''

        if req_day:
            try:
                year, month = (int(x) for x in req_day.split('-'))
                return date(year, month, 1)

            except ValueError:
                pass  # In case of an invalid format, fallback to today
    
        return datetime.today().date()


    def previous_month(self, cal_day):
        '''
        Function to get the previous month.
        '''

        first_day = cal_day.replace(day = 1)
        previous_month = first_day - timedelta(days = 1)

        return f'month={previous_month.year}-{previous_month.month}'


    def next_month(self, cal_day):
        '''
        Function to get the next month.
        '''

        days_in_month = calendar.monthrange(cal_day.year, cal_day.month)[1]
        last_day = cal_day.replace(day = days_in_month)
        next_month = last_day + timedelta(days = 1)

        return f'month={next_month.year}-{next_month.month}'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cal_day = self.get_date(self.request.GET.get('month', None))

        # Fetch only the logged-in user's events
        user_events = Event.objects.filter(
            user = self.request.user,
            start_time__year = cal_day.year,
            start_time__month = cal_day.month
        )

        event_calendar = Calendar(cal_day.year, cal_day.month)
        html_calendar = event_calendar.formatmonth(events = user_events, withyear = True)

        context['calendar'] = mark_safe(html_calendar)
        context['previous_month'] = self.previous_month(cal_day)
        context['next_month'] = self.next_month(cal_day)
        context['events'] = user_events

        return context


class EventListView(RedirectIfNotAuthenticatedMixin, ListView):
    '''
    Class-based view to list all events for the logged-in user.
    '''

    model = Event
    template_name = 'omaha_places_app/event_list.html'
    context_object_name = 'events'
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        '''
        Function to get the queryset.
        Returns only the events for the logged-in user, optionally filtered by search query.
        '''

        query = self.request.GET.get('q', '')  # Get search query from URL
        queryset = Event.objects.filter(user = self.request.user)

        if query:
            queryset = queryset.filter(name__icontains = query)  # Case-insensitive search

        return queryset

    def get_context_data(self, **kwargs):
        '''
        Function to pass additional context to the template.
        Includes the search query in the context for display in the template.
        '''
        
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass query to the template

        return context


class EventCreateView(RedirectIfNotAuthenticatedMixin, CreateView):
    '''
    Class-based view to create a new event.
    '''

    model = Event
    form_class = EventForm
    template_name = 'omaha_places_app/event.html'
    success_url = reverse_lazy('calendar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.request.GET.get('location_id')

        if location_id:
            location_value = None
            
            try: # Try to fetch as a restaurant first
                location = get_object_or_404(Restaurant, id = location_id)
                location_value = f'restaurant:{location.id}'
            except Restaurant.DoesNotExist: # If not found, try fetching as a place
                try:
                    location = get_object_or_404(Place, id = location_id)
                    location_value = f'place:{location.id}'
                except Place.DoesNotExist:
                    pass

            if location_value:
                context['form'].initial['location_object'] = location_value

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(RedirectIfNotAuthenticatedMixin, UpdateView):
    '''
    Class-based view to update an existing event.
    '''

    model = Event
    form_class = EventForm
    template_name = 'omaha_places_app/event_edit.html'
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        return Event.objects.all()
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            messages.warning(request, 'You do not have permission to delete this event.')
            return redirect('calendar')
        
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect('calendar')


class EventDeleteView(RedirectIfNotAuthenticatedMixin, DeleteView):
    '''
    Class-based view to delete an event.
    Ensures only the event owner can delete it.
    '''
    
    model = Event
    template_name = 'omaha_places_app/event_delete.html'
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        return Event.objects.all()
    
    def handle_no_permission(self):
        return redirect('calendar')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            messages.warning(request, "You do not have permission to delete this event.")
            return redirect('calendar')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''
        Handle the confirmation page
        '''

        context = {
            'event': self.get_object()
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        '''
        Handle the deletion when the user confirms
        '''

        event = self.get_object()
        event.delete()

        return HttpResponseRedirect(self.success_url)
    

def get_locations(request):
    '''
    Function to get the locations of the specified type.
    '''

    location_type = request.GET.get('type')

    if location_type == 'place':
        locations = Place.objects.all()
    elif location_type == 'restaurant':
        locations = Restaurant.objects.all()
    else:
        return JsonResponse({'error': 'Invalid location type'}, status = 400)

    data = [{'id': loc.pk, 'name': loc.name} for loc in locations]
    
    return JsonResponse({'locations': data})