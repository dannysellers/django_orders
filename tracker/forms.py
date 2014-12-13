from django import forms
from django.forms import ModelForm
import models
from datetime import date


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Customer's name: ")
	acct = forms.CharField(max_length=5, help_text="Account number: ")
	email = forms.EmailField(help_text="Email address: ")
	status = forms.CharField(widget=forms.HiddenInput(), initial=1, required=False)
	createdate = forms.DateField(widget=forms.HiddenInput(), initial=date.today(), required=False)
	closedate = forms.DateField(widget=forms.HiddenInput(), initial=date.today(), required=False)

	# An inline class that provides additional info on the form
	class Meta:
		# Links form to model object
		model = models.Customer
		fields = ('name', 'acct', 'email')


class InventoryForm(forms.ModelForm):
	quantity = forms.CharField(max_length=5, help_text="Quantity: ")
	length = forms.DecimalField(max_digits=6, initial=1.00, help_text="Length (in.): ")
	width = forms.DecimalField(max_digits=6, initial=1.00, help_text="Width (in.): ")
	height = forms.DecimalField(max_digits=6, initial=1.00, help_text="Height (in.): ")
	palletized = forms.BooleanField(initial=False, help_text="Palletized? :", required=False)
	arrival = forms.DateField(widget=forms.HiddenInput(), initial=date.today(), required=False)
	departure = forms.DateField(widget=forms.HiddenInput(), initial=date.today(), required=False)
	status = forms.CharField(widget=forms.HiddenInput(), initial=0, required=False)

	class Meta:
		model = models.Inventory

		fields = ('quantity', 'length', 'width', 'height', 'palletized')


class ItemForm(ModelForm):
	class Meta:
		model = models.Inventory