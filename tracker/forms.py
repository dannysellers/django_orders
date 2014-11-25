from django import forms
import models
from datetime import date


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Customer's name: ")
	acct = forms.CharField(max_length=5, help_text="Account number: ")
	email = forms.EmailField(help_text="Email address: ")
	status = forms.CharField(widget=forms.HiddenInput(), initial=1)
	createdate = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
	closedate = forms.DateField(widget=forms.HiddenInput(), required=False)

	# An inline class that provides additional info on the form
	class Meta:
		# Links form to model object
		model = models.Customer


class InventoryForm(forms.ModelForm):
	itemid = forms.CharField(help_text="Item ID:")
	quantity = forms.CharField(max_length=5, help_text="Quantity:")
	length = forms.DecimalField(max_digits=6, initial=1.00, help_text="Length (in.):")
	width = forms.DecimalField(max_digits=6, initial=1.00, help_text="Width (in.):")
	height = forms.DecimalField(max_digits=6, initial=1.00, help_text="Height (in.):")
	volume = forms.DecimalField(widget=forms.HiddenInput())
	palletized = forms.BooleanField(initial=False, help_text="Palletized?:")
	palletweight = forms.CharField(help_text="Pallet weight:")
	arrival = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
	status = forms.CharField(widget=forms.HiddenInput(), initial=0)  # choices?
	storage_fees = forms.IntegerField(widget=forms.HiddenInput())

	class Meta:
		model = models.Inventory

		# fields = ('quantity', 'weight', 'palletized', 'palletweight')