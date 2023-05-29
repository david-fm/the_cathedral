from django.urls import path
from . import views

app_name = 'user_system'
urlpatterns = [
    path('my_publications', views.my_publications, name='my_publications'),
]
