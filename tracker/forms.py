from datetime import date

from django import forms
from django.contrib.auth.models import User
from models import Customer, Inventory


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length = 128, help_text = "Customer's name: ")
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
	palletized = forms.BooleanField(initial = False, help_text = "Palletized? :", required = False)
	arrival = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	departure = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	status = forms.CharField(widget = forms.HiddenInput(), initial = 0, required = False)

	class Meta:
		model = Inventory

		fields = ('quantity', 'length', 'width', 'height', 'palletized')


# class ItemForm(forms.ModelForm):
# class Meta:
# 		model = models.Inventory

class UserForm(forms.ModelForm):
	username = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
