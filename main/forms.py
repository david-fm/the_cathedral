from django import forms
from django.contrib.auth.models import User
from articles.models import UserPersonalized
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserPersonalized  ######
        fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput())