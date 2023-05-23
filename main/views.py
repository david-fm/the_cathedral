from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
# Import the User object
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    INCORRECT_PASSWORD = 'Incorrect password'
    INCORRECT_FORM = 'Incorrect form'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'submit_login' in request.POST:

            # create a form instance and populate it with data from the request:
            login_form = LoginForm(request.POST)
            # check whether it's valid:
            if login_form.is_valid():
                print('Form is valid as a login form')
                # process the data in form.cleaned_data as required
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    print('User is valid, active and authenticated')
                    # redirect to a new URL:
                    return render(request, 'main/index.html')
                # redirect to a new URL:
            register_form = RegisterForm()
            print('Login Form is not valid')
            return render(request, 'main/index.html', 
                    {'login_form': login_form,
                    'register_form': register_form, 
                    'login_error_message': INCORRECT_PASSWORD})
        else:
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                print('Form is valid as a register form')
                user = register_form.save()
                user.refresh_from_db()
                login(request, user)
                
                # redirect to a new URL:
                return render(request, 'main/index.html')

            
            login_form = LoginForm()
            print('Register Form is not valid')
            return render(request, 'main/index.html', 
                    {'login_form': login_form,
                    'register_form': register_form, 
                    'register_error_message': INCORRECT_FORM})

    print('nada bien')
    # if a GET (or any other method) we'll create a blank form
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'main/index.html', {'login_form': login_form, 'register_form': register_form})