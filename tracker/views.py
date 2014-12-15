from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Customer, Inventory
# import forms


def index (request):
	context = RequestContext(request)
	context_dict = {}

	context_dict['cust_count'] = Customer.objects.count()
	context_dict['cust_act_count'] = Customer.objects.filter(status = 1).count()
	context_dict['item_count'] = Inventory.objects.count()

	storage_fee_count = 0
	no_storage_fee_count = 0
	for item in Inventory.objects.all().exclude(status = 4):
		if abs((item.arrival - date.today()).days) >= 7:
			storage_fee_count += 1
		else:
			no_storage_fee_count += 1
	context_dict['item_storage_count'] = storage_fee_count
	context_dict['item_no_storage_count'] = no_storage_fee_count

	return render_to_response('tracker/index.html', context_dict, context)


def about (request):
	context = RequestContext(request)
	context_dict = {'name': 'About'}

	return render_to_response('tracker/about.html', context_dict, context)


def register (request):
	context = RequestContext(request)
	context_dict = {}

	# Flag for template
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)

		if user_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			registered = True
		# Redirection?
		else:
			print user_form.errors
	else:
		user_form = UserForm()

	context_dict['user_form'] = user_form
	context_dict['registered'] = registered

	return render_to_response('tracker/register.html', context_dict, context)


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
			# User could have been deactivated
			if user.is_active:
				# If the user is valid and active, log in and redirect to index
				# login() is built in
				# login(request, user)
				login(request, user)
				messages.add_message(request, messages.SUCCESS, "Login successful. Welcome {}".format(user))
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.ERROR, "This account is inactive and cannot be used.")
				return HttpResponseRedirect('/')

		else:
			messages.add_message(request, messages.ERROR, "Invalid login details: {0}, {1}".format(username, password))
			return HttpResponseRedirect('/')

	# If not a POST, display login form
	else:
		return render_to_response('tracker/login.html', {}, context)


@login_required
def user_logout (request):
	logout(request)

	messages.add_message(request, messages.SUCCESS, "Logged out successfully.")
	return HttpResponseRedirect('/')