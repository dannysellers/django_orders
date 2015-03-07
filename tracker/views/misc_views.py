from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm
from ..models import *


def index (request):
    context = RequestContext(request)
    context_dict = dict()

    context_dict['cust_act_count'] = Customer.objects.filter(status = 1).count()
    context_dict['item_count'] = Inventory.objects.exclude(status = 4).count()
    context_dict['ship_count'] = Shipment.objects.exclude(status = 4).count()
    context_dict['total_item_volume'] = Inventory.objects.exclude(status = 4).aggregate(Sum('volume'))['volume__sum']

    ten_days_ago = date.today() - timedelta(days = 10)

    context_dict['item_storage_count'] = Inventory.objects.exclude(status = 4) \
        .filter(arrival__lte = ten_days_ago).count()
    context_dict['item_no_storage_count'] = Inventory.objects.exclude(status = 4) \
        .filter(arrival__range = (ten_days_ago, date.today())).count()

    return render_to_response('tracker/index.html', context_dict, context)


def register (request):
    context = RequestContext(request)
    context_dict = {}

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            messages.add_message(request, messages.SUCCESS, "User {} registered successfully".format(user.username))
            return HttpResponseRedirect('/', context)
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    context_dict['form'] = user_form
    context_dict['form_type'] = 'register'

    return render_to_response('tracker/form.html', context_dict, context)


def user_login (request):
    context = RequestContext(request)

    if request.method == 'POST':
        # Login info is provided by the form
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's built-in authentication function
        user = authenticate(username = username, password = password)

        # If no user is returned, login was unsuccessful
        if user:
            if user.is_active:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                login(request, user)
                messages.add_message(request, messages.SUCCESS,
                                     "Login successful. Welcome, {}.".format(user.first_name))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.add_message(request, messages.ERROR, "This account is inactive and cannot be used.")
                return HttpResponseRedirect('/')

        else:
            messages.add_message(request, messages.ERROR, "Invalid login details for {0}".format(username))
            return HttpResponseRedirect('/')
    else:
        return render_to_response('tracker/login.html', context)


@login_required
def user_logout (request):
    logout(request)

    messages.add_message(request, messages.SUCCESS, "Logged out successfully.")
    return HttpResponseRedirect('/')