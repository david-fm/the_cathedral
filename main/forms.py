from django import forms
from django.contrib.auth.models import User
from user_system.models import UserPersonalized
class RegisterForm(forms.ModelForm):
    """
    :class: RegisterForm

    RegisterForm is class that represents a form that allows the user to register in the system.
    """
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserPersonalized  ######
        fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
    """
    :class: LoginForm
    
    LoginForm is class that represents a form that allows the user to login in the system.
    """
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput())