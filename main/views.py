from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
# Import the User object
from django.contrib.auth.models import Group
from articles.models import UserPersonalized, Publication, BlockImage, BlockText
from django.contrib.auth import authenticate, login, logout
from functools import partial
from itertools import chain
from django.db.models import Q

def user_system_decorator_partial(func, to_render='main/index.html'):
    def wrapper(request, *args, **kwargs):
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
                        return func(request, *args, **kwargs)
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
                    user = UserPersonalized.objects.create_user(
                        username=register_form.cleaned_data['username'],
                        password=register_form.cleaned_data['password'],
                        email=register_form.cleaned_data['email'],
                    )
                    user.save()

                    #
                    group_name = 'Publishers'
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)
                    #
                    login(request, user)

                    # redirect to a new URL:
                    return func(request, *args, **kwargs)  # TODO: Redirect to the appropriate page

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
                return func(request, *args, **kwargs)

        return func(request, *args, **kwargs)

    return wrapper


decorator_index = partial(user_system_decorator_partial, to_render='main/index.html')


# Create your views here.
@decorator_index
def index(request):
    # if a GET (or any other method) we'll create a blank form
    login_form = LoginForm()
    register_form = RegisterForm()

    pubs = Publication.objects.all().filter(is_checked=True)
    pubs_relevant = sorted(pubs, key=lambda sorted_pub: sorted_pub.rate_relevance(), reverse=True)
    pubs_newer = pubs.order_by('-pub_date')
    
    three_most_relevant= pubs_relevant[:3]
    three_most_relevant = [(BlockImage.objects.filter(block__publication=publication.id).first(), publication.title, publication.id) for publication in three_most_relevant]
    sixth_newer = pubs_newer[:6]
    sixth_newer = [(BlockImage.objects.filter(block__publication=publication.id).first(), publication.title, publication.id) for publication in sixth_newer]
    return render(request, 'main/index.html', {'login_form': login_form, 'register_form': register_form, 'three_most_relevant': three_most_relevant, 'sixth_newer':sixth_newer})


decorator_search = partial(user_system_decorator_partial, to_render='main/search.html')


@decorator_search
def search(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    # Obtain the result and category
    result = request.GET.get('search')
    category = request.GET.get('category')

    
    # Obtain filter, categories and result from the previous session
    the_filter = request.session.get('filter', "no_filter")
    categories = request.session.get('categories', [])
    previous_result = request.session.get('result')
    

    if category:
        result = ""   # the "*" means we will use to indicate that the seacrh will include all the pubs with the catgeory selected
        filtered_pubs = Publication.objects.filter(is_checked=True).filter(category__icontains=category)
    else:
        new_result = result.rstrip()       # if there is " " is eliminated
        filtered_pubs = Publication.objects.filter( #if not "*" the search base will contain the pubs with a similar result in title, keyword, category or publisher
            Q(title__icontains=new_result) |
            Q(keywords__keyword__icontains=new_result) |
            Q(category__icontains=new_result) |
            Q(publisher__username__icontains=new_result)
            ).filter(is_checked=True).distinct()

    # reset filters and categories if there is another search value
    if result != previous_result:
        page_number = 1
        the_filter = "no_filter"
        categories = []
        if category:
            categories.append(category) 
        result = result + " "   # " " is added to differentiate every new search with the same input
    else:
        page_number = request.GET.get('page_number')
    print("page_number: ", page_number)
    filter_by = request.GET.get('filter_by')

    if filter_by :
    #add the filter category and value to the list of filters
        the_filter = filter_by

    categories = request.GET.getlist('filter_by_category')


    # if there are categories, we will obtain a queryset with the publications
    if categories != []:
        category_query = Q()
        for category in categories:
            category_query |= Q(category__icontains=category)
        filtered_pubs = filtered_pubs.filter(category_query).distinct()

    # if there are filters, we apply all of them
    if the_filter != "no_filter":
            filter_by = the_filter
            if filter_by == 'title':
                filtered_pubs = filtered_pubs.filter(title__icontains=new_result)
            elif filter_by == 'keyword':
                filtered_pubs = filtered_pubs.filter(keywords__keyword__icontains=new_result)
            elif filter_by == 'publisher':
                filtered_pubs = filtered_pubs.filter(publisher__username__icontains=new_result)

    order_by = request.GET.get('order_by')
    #simple_search = Publication.objects.all()
    ai_counter = filtered_pubs.filter(category__icontains="artificial-intelligence").count()
    cn_counter  = filtered_pubs.filter(category__icontains="computer-networks").count()
    os_counter = filtered_pubs.filter(category__icontains="operating-systems").count()
    c_counter =filtered_pubs.filter(category__icontains="cybersecurity").count()
    ds_counter = filtered_pubs.filter(category__icontains="data-science").count()
    if not order_by:
        filtered_pubs = filtered_pubs.order_by('-pub_date')    # Default, the order ys by pub_date
    else:
        if order_by == 'relevance':
            filtered_pubs = sorted(filtered_pubs, key=lambda pub_filtered: pub_filtered.rate_relevance(), reverse=True)

        elif order_by == 'new':
            filtered_pubs = filtered_pubs.order_by('-pub_date')

        elif order_by == 'old':
            filtered_pubs = filtered_pubs.order_by('pub_date')


    number_of_results = len(filtered_pubs)
    final_pubs = [
        (BlockImage.objects.filter(block__publication=publication.id).first(), 
         publication.title, 
         publication.id,
         BlockText.objects.filter(block__publication=publication.id).first()
         ) for publication in filtered_pubs]

    number_of_pages = number_of_results // 4

    ai = True if 'artificial-intelligence' in categories else False
    cn = True if 'computer-networks' in categories else False
    os = True if 'operating-systems' in categories else False
    c = True if 'cybersecurity' in categories else False
    ds = True if 'data-science' in categories else False
    # overwrite the session filters  , categories and result
    request.session['filter'] = the_filter
    request.session['categories'] = categories
    request.session['result'] = result
    request.session['page_number'] = page_number
    initial = (int(page_number)-1)*4+1 if int(page_number)-1 else 1
    return render(request, 'main/search.html', {
            'result': result,
            'filtered_pubs': filtered_pubs[initial-1:initial+3],
            'login_form': login_form,
            'register_form': register_form,
            'number_of_results': number_of_results,
            'final_pubs': final_pubs[initial-1:initial+3],
            'selected_filter': the_filter,
            'page_number': page_number,
            'number_of_pages': number_of_pages,
            'ai_counter': ai_counter,
            'cn_counter': cn_counter,
            'os_counter': os_counter,
            'c_counter': c_counter,
            'ds_counter': ds_counter,
            'cn': cn,
            'ai': ai,
            'os': os,
            'c': c,
            'ds': ds,
    })
    
# TODO: Make login, logout and register available for all the views

