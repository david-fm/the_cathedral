from django import forms
from django.contrib.auth.models import User
from user_system.models import UserPersonalized
class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserPersonalized  ######
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput())