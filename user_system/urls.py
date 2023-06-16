from django.urls import path
from . import views

app_name = 'user_system'
urlpatterns = [
    path('my_publications', views.my_publications, name='my_publications'),
    path('user_config', views.user_config, name='user_config'),
    path('private_data', views.user_config_private_data, name='user_config_private_data'),
    path('manage_account', views.user_config_manage_account, name='manage_account'),
    path('delete_account', views.user_config_delete_account, name='delete_account'),
    path('privacy_and_data', views.privacy_and_data, name='privacy_and_data'),
    path('review_publication', views.review_publication, name='review_publication'),
    path('do_you_want_available', views.do_you_want_available, name='do_you_want_available'),
    path('reviewing_publication', views.reviewing_publication, name='reviewing_publication'),
    #path('user/<int:user_id>', views.user_profile, name='user_profile'),
]
