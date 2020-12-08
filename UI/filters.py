import django_filters
from application.models import *
from django import forms


class FormFilter(forms.ModelForm):
    departing_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local',
                                                                     'class':'form-control'}))
    arriving_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                                                           'class': 'form-control',}))
    class Meta:
        model = flight
        fields = ('departing_date','arriving_date','departure_airport','arrival_airport')

class FlightFilters(django_filters.FilterSet):
    # one_date = django_filters.DateTimeFilter(widgets=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    # departure_airport = django_filters.ChoiceFilter(choices=('Select'))
    class Meta:
        model = flight
        # form = FormFilter
        fields = {'departure_time':['year__gt'],'arrival_time':['year__lt']}
        FILTERS_DISABLE_HELP_TEXT = False
    # def get_form_class(self):
    #     form_data = FormFilter
    #     print(form_data)
    #     return form_data