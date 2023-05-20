from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
#from .models import Article
from .models import Publication


class IndexView(generic.ListView):
    template_name = 'articles/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        """Return the last five published articles."""
        #return Article.objects.order_by('-pub_date')[:5]
        return Publication.objects.order_by('-pub_date')[:5]

def index(request):
    #latest_article_list = Article.objects.order_by('-pub_date')[:5]
    latest_article_list = Publication.objects.order_by('-pub_date')[:5]
    context = {'latest_article_list': latest_article_list}
    return render(request, 'articles/index.html', context)

def detail(request, article_id):
    return HttpResponse("You're looking at article %s." % article_id)

def results(request, article_id):
    response = "You're looking at the results of article %s."
    return HttpResponse(response % article_id)

