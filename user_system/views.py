from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import Publicate
from articles.models import Publication, BlockText
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