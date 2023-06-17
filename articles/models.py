""" 
This module contains the models of the articles app.
"""
from django.db import models
from user_system.models import UserPersonalized

# import MEDIA_ROOT

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# execute this command
# shell: exec(open('user_system/groups_and_permissions.py').read())
def user_directory_path(instance, filename):
    """
    Function to obtain the path to the file of a publication

    :param instance: instance of the publication
    :type instance: Publication
    :param filename: name of the file
    :type filename: string

    """
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.publisher.id, filename)

def directory_for_blocks(instance, filename):
    """
    Function to obtain the path to the file of a block

    :param instance: instance of the block
    :type instance: Block
    :param filename: name of the file
    :type filename: string
    """
    # file will be uploaded to MEDIA_ROOT / user_<id>/<publication_title>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.block.publication.publisher.id, instance.block.publication.title, filename)



class Publication(models.Model):
    """
    :class: Publication

    Publication is the class that represents a publication in the system.
    """
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, null=True, blank=True)
    pub_date = models.DateTimeField('date and time when the publication was published', null=True, blank=True)
    max_size = models.IntegerField(null=True, blank=True)
    pdf_version = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    html_version = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    publisher = models.ForeignKey(UserPersonalized, on_delete=models.CASCADE, related_name='publications')
    checks = models.ManyToManyField(UserPersonalized, related_name='checks', limit_choices_to={
        'available': True,
        'groups__permissions__codename': 'is_checker',
    })
    rates = models.ManyToManyField(UserPersonalized, through='Rate', related_name='rates')
    is_checked = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # function to obtain the number of rates of a publication
    def rate_count(self):
        """
        function to obtain the number of rates of a publication

        :return: number of rates of a publication
        :rtype: int
        """
        return self.rates.count()

    # function to obtain the average rate of a publication
    def rate_average(self):
        """
        function to obtain the average rate of a publication

        :return: average rate of a publication
        :rtype: float
        """
        #rates = self.rates.through.objects.filter(publication=self)
        rates = Rate.objects.filter(publication=self)
        count = rates.count()
        if count > 0:
            total = sum(rate.rate_value for rate in rates)
            average = total / count
            return average
        else:
            return 0

           # TODO: test more cases, improve if there is any better options

    # function to obtain the relevance of a publication
    def rate_relevance(self):
        """
        function to obtain the relevance of a publication

        :return: relevance of a publication
        :rtype: float
        """
        n_rate = self.rate_count()
        avg_rate = self.rate_average()
        return n_rate * (avg_rate ** avg_rate)

class Rate(models.Model):
    """
    :class: Rate

    Rate is the class that represents a rate in the system.
    """
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(UserPersonalized, on_delete=models.CASCADE)
    rate_value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)]) # the rate will be in th range of 1-5


class Keywords(models.Model):
    """
    :class: Keywords

    Keywords is the class that represents the keywords of a publication in the system.
    """
    keyword = models.TextField(max_length=255, null=True, blank=True)
    publications = models.OneToOneField(Publication, on_delete=models.CASCADE, primary_key=True)


class Block(models.Model):
    """
    :class: Block

    Block is the class that represents a block in the system.
    """
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False)
    next_block = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_formal = models.BooleanField(default=True)
    size = models.FloatField(default=0.0)





class Font(models.Model):
    """
    :class: Font

    Font is the class that represents a font in the system.
    """
    name = models.CharField(max_length=50)
    font_path = models.FileField(upload_to='fonts/')

class BlockTitle(models.Model):
    """
    :class: BlockTitle

    BlockTitle is the class that represents a title of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    title_type = models.CharField(max_length=2, default='1', blank=True, null=True)
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)


class BlockText(models.Model):
    """
    :class: BlockText

    BlockText is the class that represents a text of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(max_length=3500, blank=True, null=True)
    font_size = models.FloatField(blank=True, null=True)
    font = models.ForeignKey(Font, blank=True, null=True, on_delete=models.SET_NULL)


# to do


class BlockImage(models.Model):
    """
    :class: BlockImage

    BlockImage is the class that represents an image of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    file_path = models.FileField(upload_to=directory_for_blocks, null=True, blank=True)


class BlockVideo(models.Model):
    """
    :class: BlockVideo

    BlockVideo is the class that represents a video of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    url = models.TextField(max_length=250, null=True, blank=True)
    is_formal = models.BooleanField(default=False)


class BlockQuiz(models.Model):
    """
    :class: BlockQuiz

    BlockQuiz is the class that represents a quiz of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=250, blank=True, null=True)
    is_formal = models.BooleanField(default=False)


class Questions(models.Model):
    """
    :class: Questions

    Questions is the class that represents a question of a quiz in the system.
    """
    
    question = models.TextField(max_length=350, blank=True)
    quiz_block = models.ForeignKey(BlockQuiz, on_delete=models.CASCADE, null=False)


class Answer(models.Model):
    """
    :class: Answer

    Answer is the class that represents an answer of a question in the system.
    """
    answer = models.TextField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False)



class BlockDoi(models.Model):
    """
    :class: BlockDoi

    BlockDoi is the class that represents a doi of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    doi = models.CharField(max_length=255)


class BlockAuthors(models.Model):
    """
    :class: BlockAuthors

    BlockAuthors is the class that represents the authors of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    authors = models.ManyToManyField(UserPersonalized, blank=True)


# to do

class BlockTable(models.Model):
    """
    :class: BlockTable

    BlockTable is the class that represents a table of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(max_length=3500)
    font_size = models.FloatField()
    font = models.ForeignKey(Font, on_delete=models.SET_NULL, blank=True, null=True)



class BlockReferences(models.Model):
    """
    :class: BlockReferences
    
    BlockReferences is the class that represents the references of a block in the system.
    """
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(max_length=250, null=True, blank=True)

class Comments(models.Model):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField(max_length=3500)
