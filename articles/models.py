import os.path

from django.db import models
from django.conf import settings


# Create your models here.

def path(type_file: str):
    return os.path.join(settings.LOCAL_FILE_DIR, type_file)


class Publication(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date and time when the publication was published')
    max_size = models.IntegerField()
    pdf_version = models.FilePathField(path=path('pdf'))
    html_version = models.FilePathField(path=path('html'))
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publications')
    checks = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checked_publications')
    rates = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                              related_name='rated_publications')


class Keywords(models.Model):
    keyword = models.TextField(max_length=255)
    publications = models.ManyToManyField(Publication)





class Block(models.Model):
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False)
    next_block_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    is_formal = models.BooleanField(default=True)
    size = models.FloatField(default=0.0)

    class Meta:
        abstract = True

class Font(models.Model):
    name = models.CharField(max_length=50)
    font_path = models.FilePathField(path=path('font'))
class BlockTitle(Block):
    title = models.CharField(max_length=255)
    font_size = models.FloatField()
    font = models.ManyToManyField(Font, blank=True)


class BlockText(Block):
    text = models.CharField(max_length=3500)
    font_size = models.FloatField()
    font = models.ManyToManyField(Font, blank=True)
# to do


class BlockImage(Block):
    file_path = models.FilePathField(path=path('image'))
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
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
# to do

class BlockTable(Block):
    text = models.TextField(max_length=3500)
    font_size = models.FloatField()
    font = models.ManyToManyField(Font, blank=True)



class BlockReferences(Block):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)



