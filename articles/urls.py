from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /articles/5/
    path('<int:article_id>/', views.detail, name='detail'),
    # ex: /articles/5/results/
    path('<int:article_id>/results/', views.results, name='results'),

    path('<int:article_id>/edit/', views.edit_view, name='edit'),

    path('<int:article_id>/save/', views.save, name='save'),

    path('<int:publication_id>/create_block/<int:prev_block_id>/', views.create_block, name='create_block')

]