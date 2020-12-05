from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from application.models import *
from django.db.models import Q
from django.urls import reverse_lazy, resolve
from .filters import *
from datetime import datetime
from django.db.models import Prefetch


# Create your views here.


class SearchAndListView(LoginRequiredMixin, generic.ListView):
    model = flight
    context_object_name = 'flight_list'
    template_name = './main.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(SearchAndListView, self).get_context_data(*args, **kwargs)
        ctx['airports'] = airport.objects.all()
        ##filters
        d_time = self.request.GET.get('departure_time')
        a_time = self.request.GET.get('arrival_time')

        ctx['time1'] = d_time
        ctx['time2'] = a_time

        customer = CustomerDetails.objects.filter(user=self.request.user)
        if customer:
            ctx['customer'] = customer[0]
        print(customer)
        return ctx

    def get_queryset(self, *args, **kwargs):
        # searched_item = self.request.GET.get('Search_bar')
        filter_item = self.request.GET
        current_url = resolve(self.request.path_info).url_name

        qs = ''
        if current_url == 'all_flights':
            qs = flight.objects.select_related('airline', 'airplane', 'departure_airport', 'arrival_airport').all()
        # qs = flight.objects.all()
        if filter_item:
            ##city filters

            qs = flight.objects.filter(Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                       | Q(arrival_airport__city__iexact=filter_item['arrival_airport']))

            # apply = FlightFilters(self.request.GET,queryset=flight.objects.all())
            # qs=apply.qs
            d_time = filter_item['departure_time']
            a_time = filter_item['arrival_time']
            print(d_time)
            if (filter_item['departure_airport'] != '') & (filter_item['arrival_airport'] != ''):
                qs = flight.objects.filter(Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                           & Q(arrival_airport__city__iexact=filter_item['arrival_airport']))

            if ((d_time != '') & (a_time != '')) & (
                    (filter_item['departure_airport'] != '') | (filter_item['arrival_airport'] != '')):
                departure_time = datetime.strptime(d_time, '%Y-%m-%dT%H:%M')
                arrival_time = datetime.strptime(a_time, '%Y-%m-%dT%H:%M')

                if (filter_item['departure_airport'] != '') & (filter_item['arrival_airport'] != ''):
                    qs = flight.objects.filter(Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                               & Q(arrival_airport__city__iexact=filter_item['arrival_airport'])
                                               & (Q(departure_time__gt=departure_time)
                                                  & Q(arrival_time__lt=arrival_time)))
                # compound filter
                else:
                    qs = flight.objects.filter((Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                                | Q(arrival_airport__city__iexact=filter_item['arrival_airport']))
                                               & (Q(departure_time__gt=departure_time)
                                                  & Q(arrival_time__lt=arrival_time))
                                               )
            # both time filters
            elif (d_time != '') & (a_time != ''):
                departure_time = datetime.strptime(d_time, '%Y-%m-%dT%H:%M')
                arrival_time = datetime.strptime(a_time, '%Y-%m-%dT%H:%M')
                qs |= flight.objects.filter(Q(departure_time__gt=departure_time)
                                            & Q(arrival_time__lt=arrival_time))
            # departure time filter
            elif d_time != '':
                departure_time = datetime.strptime(d_time, '%Y-%m-%dT%H:%M')
                if qs:
                    qs = flight.objects.filter((Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                                | Q(arrival_airport__city__iexact=filter_item['arrival_airport']))
                                               & Q(departure_time__gt=departure_time))
                else:
                    qs |= flight.objects.filter(Q(departure_time__gt=departure_time)
                                                )
            # arrival time filter
            elif a_time != '':
                arrival_time = datetime.strptime(a_time, '%Y-%m-%dT%H:%M')
                if qs:
                    qs = flight.objects.filter((Q(departure_airport__city__iexact=filter_item['departure_airport'])
                                                | Q(arrival_airport__city__iexact=filter_item['arrival_airport']))
                                               & Q(arrival_time__lt=arrival_time))
                else:
                    qs |= flight.objects.filter(Q(arrival_time__lt=arrival_time))

        return qs


class MyFlights(LoginRequiredMixin, generic.ListView):
    model = flight
    context_object_name = 'flight_list'
    template_name = './main.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(MyFlights, self).get_context_data(*args, **kwargs)
        ctx['purchase'] = 'Purchase'
        ctx['airports'] = airport.objects.all()
        account = AccountCredits.objects.filter(user=self.request.user)
        ctx['total_amount'] = account[0].total_spend()
        ctx['remaining_amount'] = account[0].account_balance
        customer = CustomerDetails.objects.filter(user=self.request.user)
        if customer:
            ctx['customer'] = customer[0]
        return ctx

    def get_queryset(self):
        customer_user = CustomerDetails.objects.filter(user=self.request.user)
        if customer_user:
            x = PurchaseTicket.objects.filter(customer_email=self.request.user)
        else:
            x = PurchaseTicket.objects.filter(user=self.request.user)

        qs = {}
        for i in x:
            print(i.ticket_status)
            x = i.ticket_status  + str(i.pk)
            qs[x] = (flight.objects.get(pk=i.ticket.pk))

        return qs


class CompleteFlightView(LoginRequiredMixin, generic.DetailView):
    model = flight
    context_object_name = 'flight_detail'
    template_name = './main_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(CompleteFlightView, self).get_context_data(**kwargs)
        ctx['flights'] = flight.objects.filter(pk=self.kwargs.get('pk'))
        return ctx


def PurchaseTicketView(request, *args, **kwargs):
    selected_flight = flight.objects.get(pk=kwargs.get('pk'))
    pk = kwargs.get('pk')
    # register yourself in the the AccountCredit model before purchasing ticket
    my_acc_credit = AccountCredits.objects.get(user=request.user)
    customer_email = request.POST['customer_email']

    duplicate = PurchaseTicket.objects.filter(ticket=selected_flight, customer_email=customer_email)
    if duplicate:
        messages.warning(request, 'Can not purchase same ticket for same user!!!')
        return redirect(reverse_lazy('UI:flight_detail', kwargs={'pk': pk}))

    ##if not enough balance
    if selected_flight.price > my_acc_credit.account_balance:
        messages.warning(request, 'Not enough credit!!!')
        return redirect(reverse_lazy('UI:flight_detail', kwargs={'pk': pk}))
    # deducting the amount

    remaining_amount = my_acc_credit.account_balance - selected_flight.price
    AccountCredits.objects.filter(user=request.user).update(account_balance=remaining_amount)
    ticket_purchased = PurchaseTicket.objects.create(user=request.user, ticket=selected_flight,
                                                     customer_email=customer_email)
    ticket_purchased.save()
    return redirect(reverse_lazy('UI:my_tickets'))


class CustomerPurchase(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('UI:my_tickets')

    def get(self, request, *args, **kwargs):
        price_to_pay = float(self.kwargs.get('price'))
        selected_flight = flight.objects.get(pk=self.kwargs.get('pk'))
        print(selected_flight,selected_flight.airline)
        # register yourself in the the AccountCredit model before purchasing ticket
        my_acc_credit = AccountCredits.objects.get(user=self.request.user)
        # if not enough balance
        if price_to_pay > my_acc_credit.account_balance:
            messages.info(request, 'Not enough credit!!!')
            return redirect(reverse_lazy('UI:my_tickets'))
        # # deducting the amount
        remaining_amount = my_acc_credit.account_balance - price_to_pay
        AccountCredits.objects.filter(user=self.request.user).update(account_balance=remaining_amount)

        # changing status
        PurchaseTicket.objects.filter(customer_email=self.request.user,ticket=selected_flight).update(ticket_status='Confirmed')

        # transferring amount to agent
        agent = PurchaseTicket.objects.filter(customer_email=self.request.user,ticket=selected_flight)[0].user
        print(agent)
        previous_balance = AccountCredits.objects.get(user=agent).account_balance
        new_balance = previous_balance + price_to_pay
        AccountCredits.objects.filter(user=agent).update(account_balance=new_balance)
        return redirect(reverse_lazy('UI:my_tickets'))
