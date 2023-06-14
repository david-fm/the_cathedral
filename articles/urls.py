from django.urls import path
from articles.views import ArticleDetailView
from . import views

app_name = 'articles'
urlpatterns = [
    path('<int:pk>/', ArticleDetailView.as_view(template_name='articles/detail.html'), name='detail'),

    path('<int:article_id>/edit/', views.edit_view, name='edit'),

    path('<int:article_id>/save/', views.save, name='save'),

    path('<int:pk>/review/', views.ReviewView.as_view(), name='review'),

]