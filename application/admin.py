from django.contrib import admin
from .models import *
from django import forms


class customer_admin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'contact_number']
    ordering = ['-id']


class Airplane_form(forms.ModelForm):
    class Meta:
        model = airplane
        exclude = ('airline',)


class airplane_admin(admin.ModelAdmin):
    list_display = ['name', 'model', 'seats', 'airline', 'added_date']
    list_editable = ['seats']
    search_fields = ['referenceNumber']
    ordering = ['-id']
    form = Airplane_form

    def save_model(self, request, obj, form, change):
        airline_name = airline_staff.objects.get(user=request.user)
        form_data = form.cleaned_data
        print(form_data)
        my_airplane = airplane.objects.create(
            name=form_data['name'],
            model_year=form_data['model_year'],
            seats=form_data['seats'],
            airline=airline_name.airline,
        )
        my_airplane.save()
        return my_airplane


class airport_admin(admin.ModelAdmin):
    list_display = ['name', 'city']
    search_fields = ['name', 'city']
    ordering = ['-id']


class CustomForm(forms.ModelForm):
    class Meta:
        model = flight
        exclude = ('airline', 'user')


class flight_admin(admin.ModelAdmin):
    list_display = [
        'airline',
        'flight_num',
        'departure_airport',
        'arrival_airport',
        'departure_time',
        'arrival_time',
        'price',
        'status',
        'airplane'
    ]

    form = CustomForm
    search_fields = ['flight_num', 'airline']
    ordering = ['-id']

    def get_form(self, request, obj=None, change=None, **kwargs):
        obj = super(flight_admin, self).get_form(request, obj=obj, change=obj, **kwargs)
        logged_in_airline = airline_staff.objects.get(user=request.user)
        get_planes = airplane.objects.filter(airline=logged_in_airline.airline)
        obj.base_fields['airplane'].queryset = get_planes
        return obj

    def save_model(self, request, obj, form, change):
        airline_name = airline_staff.objects.get(user=request.user)
        form_data = form.cleaned_data
        my_flight = flight.objects.create(
            airline=airline_name.airline,
            flight_num=form_data['flight_num'],
            departure_airport=form_data['departure_airport'],
            arrival_airport=form_data['arrival_airport'],
            departure_time=form_data['departure_time'],
            arrival_time=form_data['arrival_time'],
            price=form_data['price'],
            status=form_data['status'],
            airplane=form_data['airplane'],
        )
        my_flight.save()
        return my_flight

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(airline=airline_staff.objects.get(user=request.user).airline)


# Register your models here.
admin.site.register(airline)
admin.site.register(airline_staff)
admin.site.register(airplane, airplane_admin)
admin.site.register(airport, airport_admin)
admin.site.register(flight, flight_admin)
admin.site.register(CustomerDetails, customer_admin)
admin.site.register(PurchaseTicket)
admin.site.register(AccountCredits)
