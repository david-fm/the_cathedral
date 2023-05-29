
from django.db import models
from django.conf import settings
from user_system.models import UserPersonalized

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.publisher.id, filename)

class Publication(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateTimeField('date and time when the publication was published', null=True, blank=True)
    max_size = models.IntegerField(null=True, blank=True)
    pdf_version = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    html_version = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    publisher = models.ForeignKey(UserPersonalized, on_delete=models.CASCADE, related_name='publications')
    checks = models.ManyToManyField(UserPersonalized, related_name='checks', null=True, blank=True)
    rates = models.ManyToManyField(UserPersonalized, related_name='rates', null=True, blank=True)


class Keywords(models.Model):
    keyword = models.TextField(max_length=255)
    publications = models.ManyToManyField(Publication)





class Block(models.Model):
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False)
    next_block_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_formal = models.BooleanField(default=True)
    size = models.FloatField(default=0.0)

    class Meta:
        abstract = True

class Font(models.Model):
    name = models.CharField(max_length=50)
    font_path = models.FileField(upload_to=user_directory_path)

class BlockTitle(Block):
    title = models.CharField(max_length=255)
    font_size = models.FloatField()
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)


class BlockText(Block):
    text = models.TextField(max_length=3500, blank=True, null=True)
    font_size = models.FloatField(blank=True, null=True)
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)
# to do


class BlockImage(Block):
    file_path = models.FileField(upload_to=user_directory_path)
    name = models.TextField(max_length=255)
    width = models.FloatField()
    height = models.FloatField()


class BlockVideo(Block):
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    url = models.TextField(max_length=250)
    is_formal = models.BooleanField(default=False)


class BlockQuiz(Block):
    name = models.TextField(max_length=250)
    is_formal = models.BooleanField(default=False)


class Questions(models.Model):
    question = models.TextField(max_length=350)
    quiz_block_id = models.ForeignKey(BlockQuiz, on_delete=models.CASCADE, null=False)


class Answer(models.Model):
    answer = models.TextField(max_length=255)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False)



class BlockDoi(Block):
    doi = models.CharField(max_length=255)


class BlockAuthors(Block):
    url_authors = models.TextField(max_length=250)


class Author(models.Model):
    authors = models.ForeignKey(BlockAuthors, on_delete=models.CASCADE, null=False)
    publisher = models.ForeignKey(UserPersonalized, on_delete=models.CASCADE, null=False)
# to do

class BlockTable(Block):
    text = models.TextField(max_length=3500)
    font_size = models.FloatField()
    font = models.ForeignKey(Font, on_delete=models.SET_NULL, blank=True, null=True)



class BlockReferences(Block):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(UserPersonalized)



