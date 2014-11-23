from django import forms
import models
from datetime import date


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length=128, label="Customer's name: ")
	acct = forms.CharField(max_length=5, label="Account number: ")
	email = forms.EmailField(label="Email address: ")
	status = forms.CharField(widget=forms.HiddenInput(), initial=1)
	createdate = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
	closedate = forms.DateField(widget=forms.HiddenInput(), required=False)

	# An inline class that provides additional info on the form
	class Meta:
		# Links form to model object
		model = models.Customer


class InventoryForm(forms.ModelForm):
	itemid = forms.CharField(label="Item ID:")
	quantity = forms.CharField(max_length=5, label="Quantity:")
	weight = forms.CharField(max_length=4, label="Weight")
	palletized = forms.BooleanField(initial=False, label="Palletized?:")
	palletweight = forms.CharField(label="Pallet weight:")
	arrival = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
	status = forms.CharField(widget=forms.HiddenInput(), initial=0)  # choices?

	class Meta:
		model = models.Inventory
