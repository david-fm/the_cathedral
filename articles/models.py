
from django.db import models
from django.conf import settings
from user_system.models import UserPersonalized
# import MEDIA_ROOT
from django.conf import settings

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.publisher.id, filename)

def directory_for_blocks(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<publication_title>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.block.publication.publisher.id, instance.block.publication.title, filename)



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
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False)
    next_block = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_formal = models.BooleanField(default=True)
    size = models.FloatField(default=0.0)


class Font(models.Model):
    name = models.CharField(max_length=50)
    font_path = models.FileField(upload_to='fonts/')

class BlockTitle(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=255)
    title_type = models.CharField(max_length=2, default='1', blank=True)
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)


class BlockText(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(max_length=3500, blank=True, null=True)
    font_size = models.FloatField(blank=True, null=True)
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)
# to do


class BlockImage(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    file_path = models.FileField(upload_to=directory_for_blocks)


class BlockVideo(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    url = models.TextField(max_length=250)
    is_formal = models.BooleanField(default=False)


class BlockQuiz(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=250)
    is_formal = models.BooleanField(default=False)


class Questions(models.Model):
    question = models.TextField(max_length=350)
    quiz_block = models.ForeignKey(BlockQuiz, on_delete=models.CASCADE, null=False)


class Answer(models.Model):
    answer = models.TextField(max_length=255)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False)



class BlockDoi(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    doi = models.CharField(max_length=255)


class BlockAuthors(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    authors = models.ManyToManyField(UserPersonalized)


# to do

class BlockTable(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(max_length=3500)
    font_size = models.FloatField()
    font = models.ForeignKey(Font, on_delete=models.SET_NULL, blank=True, null=True)



class BlockReferences(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(UserPersonalized)



