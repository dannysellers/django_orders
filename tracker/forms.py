from django import forms
from django.contrib.auth.models import User as auth_User
from models import Customer, Inventory
from datetime import date


class CustomerForm(forms.ModelForm):
	name = forms.CharField(max_length = 128, help_text = "Name:")
	acct = forms.CharField(max_length = 5, help_text = "Account number:")
	email = forms.EmailField(help_text = "Email address:")

	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['name', 'email', 'acct']

	class Meta:
		model = Customer
		fields = ('name', 'acct', 'email')


class InventoryForm(forms.ModelForm):
	quantity = forms.CharField(max_length = 5, help_text = "Quantity:")
	length = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Length (in.):")
	width = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Width (in.):")
	height = forms.DecimalField(max_digits = 6, initial = 1.00, help_text = "Height (in.):")
	palletized = forms.BooleanField(initial = False, help_text = "Palletized?: ", required = False)
	arrival = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	departure = forms.DateField(widget = forms.HiddenInput(), initial = date.today(), required = False)
	status = forms.CharField(widget = forms.HiddenInput(), initial = 0, required = False)

	class Meta:
		model = Inventory
		fields = ('quantity', 'length', 'width', 'height', 'palletized')


class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Username:")
	first_name = forms.CharField(help_text="First Name:")
	last_name = forms.CharField(help_text="Last Name:")
	email = forms.CharField(help_text="Email:")
	password = forms.CharField(widget = forms.PasswordInput(), help_text="Password:")

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['username', 'password', 'first_name', 'last_name', 'email']

	class Meta:
		model = auth_User
		fields = ('username', 'email', 'password')
