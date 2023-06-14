from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
# Import the User object
from django.contrib.auth.models import Group
from articles.models import UserPersonalized, Publication
from django.contrib.auth import authenticate, login, logout
from functools import partial
from itertools import chain
from django.db.models import Q

def user_system_decorator_partial(func, to_render='main/index.html'):
    """ 
    Decorator for the user system.
    It checks if the user is logged in and if it is, it redirects to the main page.
    Otherwise, it redirects to the login page.

    :param func: function to be decorated
    :type func: function
    :param to_render: page to be rendered
    :type to_render: string
    """
    def wrapper(request, *args, **kwargs):
        """
        Wrapper for the decorator.

        :param request: request
        :type request: HttpRequest
        :param args: arguments
        :type args: list
        :param kwargs: keyword arguments
        :type kwargs: dict
        """
        INCORRECT_PASSWORD = 'Incorrect password'
        INCORRECT_FORM = 'Incorrect form'
        print('method: ' + request.method)
        print('request: ' + str(request.GET))
        if request.method == 'POST':
            print('POST')
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
                    return render(request, to_render)  # TODO: Redirect to the appropriate page

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
    """
    View for the index page.

    :param request: request
    :type request: HttpRequest  

    """
    # if a GET (or any other method) we'll create a blank form
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'main/index.html', {'login_form': login_form, 'register_form': register_form})


decorator_search = partial(user_system_decorator_partial, to_render='main/search.html')


@decorator_search
def search(request):
    """
    View for the search page.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse  

    """

    login_form = LoginForm()
    register_form = RegisterForm()

    # Obtain the result and category
    result = request.GET.get('search')
    category = request.GET.get('category')

    # Obtain filter, categories and result from the previous session
    filters = request.session.get('filters', [])
    categories = request.session.get('categories', [])
    previous_result = request.session.get('result')


    if category:
        result = "*"+category   # the "*" means we will use to indicate that the seacrh will include all the pubs with the catgeory selected

    if result.startswith('*'):  # if "*"  the filtered pbs will have as base all the pubs with the category
        filtered_pubs = Publication.objects.all()
        new_result = result.lstrip('*').replace(' ', '')    # also we eliminate the "*" and " " to obtain only the category to filter
        filtered_pubs = filtered_pubs.filter(category__icontains=new_result)
    else:
        new_result = result.rstrip()       # if there is " " is eliminated
        filtered_pubs = Publication.objects.filter( #if not "*" the search base will contain the pubs with a similar result in title, keyword, category or publisher
            Q(title__icontains=new_result) |
            Q(keywords__keyword__icontains=new_result) |
            Q(category__icontains=new_result) |
            Q(publisher__username__icontains=new_result)
            ).distinct()

    # reset filters and categories if there is another search value
    if result != previous_result:
        filters = []
        categories = []
        result = result + " "   # " " is added to differentiate every new search with the same input


    filter_by = request.GET.get('filter_by')
    filter_value = request.GET.get('filter_value')

    if filter_by and filter_by != "_":
    # if  no_filter is selected, filters will be reseted
        if filter_by == 'no_filter':
            filters = []
    # else we add the filter category and value to the list of filters
        elif filter_value :
            filters.append((filter_by, filter_value))

    selected_categories = request.GET.getlist('filter_by_category')

    # if no_category is selected, the list o categories will be reseted
    if selected_categories and "_" not in selected_categories:
        if "no_category" in selected_categories:
            categories = []
        else: # else we add all new categories
            categories.extend(selected_categories)

    # if there are categories, we will obtain a queryset with the publications
    if categories != []:
        category_query = Q()
        for category in categories:
            category_query |= Q(category__icontains=category)
        filtered_pubs = filtered_pubs.filter(category_query).distinct()

    # if there are filters, we apply all of them
    if filters != []:
        for filter_item in filters:
            filter_by, filter_value = filter_item
            if filter_by == 'title':
                filtered_pubs = filtered_pubs.filter(title__icontains=filter_value)
            elif filter_by == 'keyword':
                filtered_pubs = filtered_pubs.filter(keywords__keyword__icontains=filter_value)
            elif filter_by == 'publisher':
                filtered_pubs = filtered_pubs.filter(publisher__username__icontains=filter_value)

    order_by = request.GET.get('order_by')

    if not order_by:
        filtered_pubs = filtered_pubs.order_by('-pub_date')    # Default, the order ys by pub_date
    else:
        if order_by == 'relevance':
            filtered_pubs = sorted(filtered_pubs, key=lambda pub_filtered: pub_filtered.rate_relevance(), reverse=True)

        elif order_by == 'new':
            filtered_pubs = filtered_pubs.order_by('-pub_date')

        elif order_by == 'old':
            filtered_pubs = filtered_pubs.order_by('pub_date')




    # overwrite the session filters  , categories and result
    request.session['filters'] = filters
    request.session['categories'] = categories
    request.session['result'] = result


    return render(request, 'main/search.html', {
        'result': result,
        'filtered_pubs': filtered_pubs,
        'login_form': login_form,
        'register_form': register_form
    })
# TODO: Make login, logout and register available for all the views
