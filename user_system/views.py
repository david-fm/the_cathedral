from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from articles.models import Publication, BlockText, Block, Keywords, BlockImage
from .forms import Publicate, UserConfig, UserConfigPrivateData, UserConfigPassword
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


# Create your views here.
@login_required
def my_publications(request):
    """
    View for the publisher's publications.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = Publicate(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            post = Publication(title=title, publisher=request.user, category=category)
            post.save()
            # 
            # ...
            # redirect to a new URL:
            return redirect('articles:edit', article_id=post.id)
    else:
        form = Publicate()
        # Get the publications from the user
        my_publications = Publication.objects.filter(publisher=request.user)
        publications = {}
        for publication in my_publications:
            # Get the first image, the first title and the first text block
            # image are blocks referenced by the model BlockImage
            image = BlockImage.objects.filter(block__publication=publication.id).first()
            # text are blocks referenced by the model BlockText
            text = BlockText.objects.filter(block__publication=publication.id).first()
            publications[publication] = (image, text)
    return render(request, 'user_system/my_publications.html', {'form': form, 'publications': publications})


@login_required
def user_config(request):
    """
    View for the user's configuration.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = UserConfig(request.POST, request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required

            name = form.cleaned_data['first_name']
            surname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            website = form.cleaned_data['website']
            biography = form.cleaned_data['biography']
            image = form.cleaned_data['image']

            request.user.image = image
            request.user.first_name = name
            request.user.last_name = surname
            request.user.email = email
            request.user.website = website
            request.user.biography = biography
            request.user.save()

            # 
            # ...
            # redirect to a new URL:
    form = UserConfig(instance=request.user)
    return render(request, 'user_system/public_profile.html', {'form': form})


@login_required
def user_config_private_data(request):
    """
    function for the user's configuration of private data.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = UserConfigPrivateData(request.POST)
        if form.is_valid():
            request.user.gender = form.cleaned_data['gender']
            request.user.country = form.cleaned_data['country']
            request.user.language = form.cleaned_data['language']
            request.user.save()

    form = UserConfigPrivateData(instance=request.user)
    return render(request, 'user_system/personal_information.html', {'form': form})


@login_required
def user_config_manage_account(request):
    """
    function for the user's configuration managing their account.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """

    if request.method == 'POST':
        form = UserConfigPassword(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()

    form = UserConfigPassword()
    return render(request, 'user_system/manage_account.html', {'form': form})


@login_required
def user_config_delete_account(request):
    """
    function for the user's configuration deleting their account.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        request.user.delete()
        return redirect('main:index')
    return redirect('user_system:manage_account')


@login_required
def privacy_and_data(request):
    """
    function for the privacy and data page.

    :param request: request
    :type request: HttpRequest
    :return: render
    :rtype: HttpResponse
    """
    return render(request, 'user_system/privacy_and_data.html')


@login_required
# @permission_required('articles.is_checker', raise_exception=True)
def review_publication(request):
    if not request.user.is_authenticated:
        return redirect('main:index')
    if not request.user.has_perm('user_system.is_checker'):
        return HttpResponseForbidden(
            'You do not have the required permissions. This option is only available for checkers')

    return render(request, 'user_system/review_publication.html', {
        'available': request.user.available
    })


@login_required
def do_you_want_available(request):

    if not request.user.is_authenticated:
            return redirect('main:index')
    
    if not request.user.has_perm('user_system.is_checker'):
        return HttpResponseForbidden(
            'You do not have the required permissions. This option is only available for checkers')

    if request.method == 'POST':
        availability = request.POST.get('available')
        if availability == 'yes':
            checker = request.user
            checker.available = True
            checker.save()
            return render(request, 'user_system/reviewing_publication.html')
        elif availability == 'no':
            return render(request, 'user_system/my_publications.html')

    return render(request, 'user_system/do_you_want_available.html')


@login_required
# @permission_required('articles.is_checker', raise_exception=True)
def reviewing_publication(request):
    if not request.user.is_authenticated:
        return redirect('main:index')

    if not request.user.has_perm('user_system.is_checker'):
        return HttpResponseForbidden('You do not have permissions required')
    checker = request.user
    pubs = Publication.objects.all().filter(checks=checker, is_checked=False)
    pubs.order_by('pub_date')  # older first
    pubs = [(BlockImage.objects.filter(block__publication=publication.id).first(), publication.title,
             BlockText.objects.filter(block__publication=publication.id).first(), publication.id) for publication in
            pubs]

    return render(request, 'user_system/reviewing_publication.html', {
        'pubs': pubs
    })



