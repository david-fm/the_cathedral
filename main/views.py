from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
# Import the User object
from django.contrib.auth.models import Group
from articles.models import UserPersonalized, Publication
from django.contrib.auth import authenticate, login, logout
from functools import partial

def user_system_decorator_partial(func, to_render='main/index.html'):
    def wrapper(request, *args, **kwargs):
        INCORRECT_PASSWORD = 'Incorrect password'
        INCORRECT_FORM = 'Incorrect form'
        print('method: '+request.method)
        print('request: '+str(request.GET))
        if request.method == 'POST':
            print ('POST')
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
                        return render(request, to_render)
                    # redirect to a new URL:
                register_form = RegisterForm()
                print('Login Form is not valid')
                return render(request, to_render, 
                        {'login_form': login_form,
                        'register_form': register_form, 
                        'login_error_message': INCORRECT_PASSWORD})
            elif 'submit_register' in request.POST:
                register_form = RegisterForm(request.POST)

                if register_form.is_valid():
                    print('Form is valid as a register form')
                    user = register_form.save()
                    user.refresh_from_db()
                    #
                    group_name = 'Publishers'
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                    #
                    login(request, user)
                    
                    # redirect to a new URL:
                    return render(request, to_render) # TODO: Redirect to the appropriate page

                
                login_form = LoginForm()
                print('Register Form is not valid')
                return render(request, to_render, 
                        {'login_form': login_form,
                        'register_form': register_form, 
                        'register_error_message': INCORRECT_FORM})
            elif 'submit_logout' in request.POST:
                logout(request)
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, to_render,
                        {'login_form': login_form,
                        'register_form': register_form})
            
        return func(request, *args, **kwargs)
    return wrapper

decorator_index = partial(user_system_decorator_partial, to_render='main/index.html')
# Create your views here.
@decorator_index
def index(request):
    # if a GET (or any other method) we'll create a blank form
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'main/index.html', {'login_form': login_form, 'register_form': register_form})

decorator_search = partial(user_system_decorator_partial, to_render='main/search.html')

@decorator_search
def search(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    
    print(request.GET)
    result = request.GET.get('search')

    pubs = Publication.objects.filter(title__icontains=result).order_by('-pub_date')
    return render(request, 'main/search.html', {'result': result,'pubs': pubs, 'login_form': login_form, 'register_form': register_form})

# TODO: Make login, logout and register available for all the views