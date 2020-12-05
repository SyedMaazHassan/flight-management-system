import django_filters
from application.models import *
from django import forms


# class FormFilter(forms.ModelForm):
#     departing_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local',
#                                                                      'class':'form-control'}))
#     arriving_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
#                                                                            'class': 'form-control',}))
#     class Meta:
#         model = flight
#         fields = ('departing_date','arriving_date','departure_airport','arrival_airport')

class FlightFilters(django_filters.FilterSet):
    # one_date = django_filters.DateTimeFilter(widgets=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = flight
        # form = FormFilter
        fields = ('departure_time','arrival_time','departure_airport','arrival_airport')
