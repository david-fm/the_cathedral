from django.urls import path

from . import views
from .views import my_view

app_name = 'articles'
urlpatterns = [
    path('<int:article_id>/', views.detail, name='detail'),

    path('<int:article_id>/edit/', views.edit_view, name='edit'),

    path('<int:article_id>/save/', views.save, name='save'),
    path('my-view/', my_view, name='my-view'),

]