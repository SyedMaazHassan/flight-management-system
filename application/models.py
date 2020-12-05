from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.core.validators import RegexValidator
from django.db.models import Q


# Create your models here.

class airline(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    isActive = models.BooleanField(default=True)
    added_date = models.DateTimeField(default=datetime.now(), editable=False)

    def __str__(self):
        return f'{self.name} - ({self.country})'


class airline_staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    airline = models.ForeignKey(airline, on_delete=models.CASCADE)


class airplane(models.Model):
    name = models.CharField(max_length=150)
    model_year = models.CharField(max_length=150)
    seats = models.IntegerField(default=30)
    airline = models.ForeignKey(airline, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now(), editable=False)

    def __str__(self):
        return f'{self.name} ({self.model_year})'


class airport(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name} ({self.city})'


class flight(models.Model):
    airline = models.ForeignKey(airline, on_delete=models.CASCADE, null=True)
    flight_num = models.IntegerField()
    departure_airport = models.ForeignKey(airport, on_delete=models.CASCADE, related_name="Departure")
    arrival_airport = models.ForeignKey(airport, on_delete=models.CASCADE, related_name="Arrival")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.FloatField()
    status = models.CharField(max_length=150, choices=[('upcoming', 'upcoming'), ('in progress', 'in progress'),
                                                       ('delayed', 'delayed')], default='upcoming')
    airplane = models.ForeignKey(airplane, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='PurchaseTicket')

    def __str__(self):
        return 'From {} to {} '.format(self.departure_airport, self.arrival_airport)


class PurchaseTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_holder',)
    ticket = models.ForeignKey(flight, on_delete=models.CASCADE, related_name='ticket_booked',unique=False)
    customer_email = models.CharField(max_length=100, default='name')
    ticket_status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')],
                                     default='Pending')

    # class Meta:
    #     unique_together = ('user', 'ticket')

    def __str__(self):
        return '{} booked by {}'.format(self.ticket.flight_num, self.user.username)


class AccountCredits(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.IntegerField(default=500)

    def __str__(self):
        return "{}$ credit in {}'s account".format(self.account_balance, self.user.username)

    def total_spend(self):
        total_tickets_purchased = PurchaseTicket.objects.filter(Q(user=self.user))
        toatl_confirmed_ticket_purchased = PurchaseTicket.objects.filter(Q(customer_email=self.user))
        total_price = 0
        customer_spend = 0
        for c_ticket in toatl_confirmed_ticket_purchased:
            if c_ticket.ticket_status!='Pending':
                customer_spend +=c_ticket.ticket.price


        for ticket in total_tickets_purchased:
            total_price += ticket.ticket.price

        return {'agent_spend':total_price,'customer_spend':customer_spend}

    class Meta:
        verbose_name_plural = 'AccountCredit'


class CustomerDetails(models.Model):
    number_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                  message=
                                  "Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_user')
    contact_number = models.IntegerField(validators=[number_regex])
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'CustomerDetails'

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
