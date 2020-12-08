from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
import json
import os


# main page function

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if airline_staff.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('admin:index'))

    return redirect(reverse('UI:home'))


# function for signup

def signup(request, status):
    if status not in ['customer', 'booking-agent', 'airline-staff']:
        return redirect("index")

    context = {
        'status': status
    }

    if status == "airline-staff":
        all_airlines = airline.objects.all()
        context['all_airlines'] = all_airlines

    if status == 'booking-agent':
        print(status)
        return render(request, 'signup.html', context)

    return render(request, "signup.html", context)


def create_account(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']

        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        status = request.POST["status"]
        print(status)
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,

        }

        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                return redirect("signup/" + status)

            # actual creating accounts
            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            if status == "booking-agent":
                print('inside booking section')
                setting_account_credit = AccountCredits.objects.create(user=user, account_balance=11500)
                setting_account_credit.save()
                user.save()

            if status == "airline-staff":
                given_airline_id = int(request.POST['airline'])
                given_airline = airline.objects.get(id=given_airline_id)

                user.is_staff = True
                user.save()

                my_group = Group.objects.get(name='airline_staff')
                my_group.user_set.add(user)

                new_airline_staff = airline_staff(user=user, airline=given_airline)
                new_airline_staff.save()

            if status == "customer":
                try:
                    contact_number = request.POST['contact_number']
                    gender = request.POST['gender']
                    customer = CustomerDetails.objects.create(user=user, contact_number=contact_number, gender=gender)
                    setting_account_credit = AccountCredits.objects.create(user=user, account_balance=1500)
                    setting_account_credit.save()
                    customer.save()
                except:
                    messages.warning(request, 'Invalid phone number')
                    return redirect('signup/' + status)

            messages.info(request, "You have been registered successfully!")
            return redirect("login")

        else:
            messages.info(request, "Your pasword doesn't match!")
            return redirect("signup/" + status)


# function for login

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return render(request,"login.html",{'logout':'logout'})
