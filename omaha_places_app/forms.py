from django import forms
from .models import Comment, Event, Place, Restaurant
from django.contrib.contenttypes.models import ContentType

class CommentForm(forms.ModelForm):
    '''
    Form for creating a new comment.
    '''

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        labels = {
            'text': '',
        }

class EventForm(forms.ModelForm):
    '''
    Form for creating a new event.
    '''
    
    location_object = forms.ChoiceField(choices=[], required=True, label='Select Venue')

    class Meta:
        model = Event
        fields = ['name', 'start_time', 'end_time', 'description']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY HH:MM:SS', 'class': 'form-control datetimepicker', 'id': 'id_start_time'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY HH:MM:SS', 'class': 'form-control datetimepicker', 'id': 'id_end_time'})
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        # Fetch all venues
        places = [(f'place:{p.pk}', f'{p.name}') for p in Place.objects.all()]
        restaurants = [(f'restaurant:{r.pk}', f'{r.name}') for r in Restaurant.objects.all()]
        self.fields['location_object'].choices = places + restaurants

        # If editing an existing event, pre-select current
        if self.instance.pk:
            model_name = self.instance.content_type.model
            object_id = self.instance.object_id
            self.fields['location_object'].initial = f'{model_name}:{object_id}'

    def clean(self):
        cleaned_data = super().clean()
        loc_value = cleaned_data.get('location_object')

        if not loc_value:
            raise forms.ValidationError('You must select a venue.')

        model_name, obj_id = loc_value.split(':')
        content_type = ContentType.objects.get(model=model_name)
        self.instance.content_type = content_type
        self.instance.object_id = obj_id

        return cleaned_data