from django.urls import path
from .views import *

app_name = 'UI'

urlpatterns = [
    path('', SearchAndListView.as_view(), name='home'),
    path('detail_flight/<int:pk>/', CompleteFlightView.as_view(), name='flight_detail'),
    path('search/', SearchAndListView.as_view(), name='flight_search'),
    path('all-flights/<flights>/',SearchAndListView.as_view(),name='all_flights'),
    path('purchase-ticket/<int:pk>/', PurchaseTicketView, name='ticket_purchase'),
    path('customer/purchase/<int:pk>/<price>/',CustomerPurchase.as_view(),name='customer_purchase'),
    path('my-tickets/',MyFlights.as_view(),name='my_tickets'),
]
