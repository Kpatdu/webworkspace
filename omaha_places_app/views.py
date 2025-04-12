from django.views.generic import TemplateView
from .mixins import AllImageAPIKeyMixin


class HomeView(AllImageAPIKeyMixin, TemplateView):
    '''
    Class-based view to render the home page.
    '''

    template_name = 'omaha_places_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_images'] = self.get_images_with_api_key()

        return context


class AboutUsView(AllImageAPIKeyMixin, TemplateView):
    '''
    Class-based view to render the about us page.
    '''
    
    template_name = 'omaha_places_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_images'] = self.get_images_with_api_key()

        return context