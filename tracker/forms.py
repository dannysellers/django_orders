from django import forms
import models
from datetime import date


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Customer's name:")
	acct = forms.CharField(max_length=5, help_text="Account number:")
	email = forms.EmailField()

	# An inline class that provides additional info on the form
	class Meta:
		# Links form to model object
		model = models.Customer


class InventoryForm(forms.ModelForm):
	itemid = forms.CharField(help_text="Item ID:")
	quantity = forms.CharField(max_length=5, help_text="Quantity:")
	weight = forms.CharField(max_length=4, help_text="Weight")
	palletized = forms.BooleanField(initial=False, help_text="Palletized?:")
	palletweight = forms.CharField(help_text="Pallet weight:")
	arrival = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
	status = forms.CharField(widget=forms.HiddenInput(), initial=0)  # choices?

	class Meta:
		model = models.Inventory
