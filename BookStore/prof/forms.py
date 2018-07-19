from django import forms

class RegistrationForm(forms.Form):
    First_Name = forms.CharField(label = 'First Name', max_length= 100)
    Last_Name = forms.CharField(label = 'Last Name', max_length= 100)
    Username = forms.CharField(label='Username', max_length=100)
    Email = forms.EmailField(label ='Email')
    Address =forms.CharField(label = 'Address(Street)', max_length=60)
    City = forms.CharField(label='Address(City)', max_length=50)
    Zip_Code =forms.IntegerField(label='Zip Code')
    psw = forms.CharField(widget=forms.PasswordInput, label='Password')
    psw_repeat = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

class LoginForm(forms.Form):
    Username = forms.CharField(label='Username', max_length=100)
    Password = forms.CharField(widget=forms.PasswordInput, label='Password')

class AddReservedCardForm(forms.Form):
    C_card_number = forms.CharField(max_length = 24)
    CVV = forms.CharField(max_length=8)
    Exp_month = forms.CharField(max_length=2)
    Exp_year = forms.CharField(max_length=4)
    Fname =  forms.CharField(max_length=32)
    Lname = forms.CharField(max_length=32)
    Mname = forms.CharField(max_length=32)

class AddPreferredCardForm(forms.Form):
    C_card_number = forms.CharField(max_length = 24)
    CVV = forms.CharField(max_length=8)
    Exp_month = forms.CharField(max_length=2)
    Exp_year = forms.CharField(max_length=4)
    Fname =  forms.CharField(max_length=32)
    Lname = forms.CharField(max_length=32)
    Mname = forms.CharField(max_length=32)
