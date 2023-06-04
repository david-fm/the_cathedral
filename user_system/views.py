from django.shortcuts import render
from django.contrib.auth.decorators import login_required
<<<<<<< Updated upstream
from .forms import Publicate
from articles.models import Publication, BlockText
=======
from .forms import Publicate, UserConfig, UserConfigPrivateData, UserConfigPassword
from articles.models import Publication, BlockText, Block
>>>>>>> Stashed changes
from django.shortcuts import redirect

# Create your views here.
@login_required
def my_publications(request):
    if request.method == 'POST':
        form = Publicate(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data['title']
            post = Publication(title=title, publisher=request.user)
            post.save()
            block = BlockText(publication_id=post, size=0.0)
            block.save()
            # 
            # ...
            # redirect to a new URL:
            return redirect('articles:edit', article_id=post.id)
    else:
        form = Publicate()
    return render(request, 'user_system/my_publications.html', {'form': form})

@login_required
def user_config(request):
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
    if request.method == 'POST':
        form = UserConfigPassword(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
    
    form = UserConfigPassword()
    return render(request, 'user_system/manage_account.html', {'form': form})

@login_required
def user_config_delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('main:index')
    return redirect('user_system:manage_account')

@login_required
def privacy_and_data(request):
    return render(request, 'user_system/privacy_and_data.html')