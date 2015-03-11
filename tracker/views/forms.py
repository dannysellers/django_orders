from django import forms
from django.contrib.auth.models import User
from ..models import Customer, Inventory
from datetime import date


class CustomerForm(forms.ModelForm):
    """
    Form used to create new Customer objects (and thus new Users
    in the Customer permissions group)
    """
    first_name = forms.CharField(max_length = 128, help_text = "First Name:")
    last_name = forms.CharField(max_length = 128, help_text = "Last Name:")
    acct = forms.IntegerField(max_value = 99999, help_text = "Account number:")
    email = forms.EmailField(help_text = "Email address (used for login):")
    password = forms.CharField(widget = forms.PasswordInput(), help_text = "Password:")

    def __init__ (self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first_name', 'last_name', 'acct', 'email', 'password']

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'acct', 'email', 'password')


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
    """
    Form used to create new Operators (Users not associated with
    any Customer object)
    """
    username = forms.CharField(help_text = "Username:")
    first_name = forms.CharField(help_text = "First Name:")
    last_name = forms.CharField(help_text = "Last Name:")
    email = forms.CharField(help_text = "Email:")
    password = forms.CharField(widget = forms.PasswordInput(), help_text = "Password:")

    def __init__ (self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username', 'password', 'first_name', 'last_name', 'email']

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
