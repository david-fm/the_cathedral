from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('<int:article_id>/', views.detail, name='detail'),

    path('<int:article_id>/edit/', views.edit_view, name='edit'),

    path('<int:article_id>/save/', views.save, name='save'),

    path('<int:publication_id>/create_block/<int:prev_block_id>/', views.create_block, name='create_block')

]