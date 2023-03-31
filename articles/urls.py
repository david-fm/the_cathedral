from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /articles/5/
    path('<int:article_id>/', views.detail, name='detail'),
    # ex: /articles/5/results/
    path('<int:article_id>/results/', views.results, name='results'),

]