from datetime import date

from django import forms
from django.contrib.auth.models import User as auth_User
from models import *


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length = 128, help_text = "Name: ")
	acct = forms.CharField(max_length = 5, help_text = "Account number: ")
	email = forms.EmailField(help_text = "Email address: ")
	status = forms.CharField(widget = forms.HiddenInput(), initial = 1, required = False)
	createdate = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	closedate = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)

	# An inline class that provides additional info on the form
	class Meta:
		# Links form to model object
		model = Customer
		fields = ('name', 'acct', 'email')


class InventoryForm(forms.ModelForm):
	quantity = forms.CharField(max_length = 5, help_text = "Quantity: ")
	length = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Length (in.): ")
	width = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Width (in.): ")
	height = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Height (in.): ")
	palletized = forms.BooleanField(initial = False, help_text = "Palletized?: ", required = False)
	arrival = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	departure = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	status = forms.CharField(widget = forms.HiddenInput(), initial = 0, required = False)

	class Meta:
		model = Inventory
		fields = ('quantity', 'length', 'width', 'height', 'palletized')


# class ShipmentForm(forms.ModelForm):
# 	palletized = forms.BooleanField(initial = False, help_text = 'Palletized: ', required = False)
# 	labor_time = forms.IntegerField(min_value = 1, help_text="Labor time: ", widget=forms.NumberInput)
# 	notes = forms.CharField(help_text="Notes: ", widget=forms.Textarea)
# 	tracking_number = forms.CharField(max_length = 30, required = True, help_text="Tracking number: ")
#
# 	class Meta:
# 		model = Shipment
# 		fields = ('labor_time', 'palletized', 'tracking_number', 'notes')


class OptExtraForm(forms.ModelForm):
	description = forms.TextInput()
	quantity = forms.CharField(max_length = 5, help_text = "Quantity: ")
	unit_cost = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Unit cost: ")

	class Meta:
		model = OptExtras


class UserForm(forms.ModelForm):
	username = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = auth_User
		fields = ('username', 'email', 'password')
