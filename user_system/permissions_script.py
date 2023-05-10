from articles.models import Article
from articles.views import MyPublicationsView, EditPublicationView, VerifyPublicationView, GivingFeedbackView
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_types = [ContentType.objects.get_for_model(Article),
                 ContentType.objects.get_for_model(MyPublicationsView),
                 ContentType.objects.get_for_model(EditPublicationView),
                 ContentType.objects.get_for_model(VerifyPublicationView),
                 ContentType.objects.get_for_model(GivingFeedbackView),]


permissions = [Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_types,)
]
