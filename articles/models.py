from django.db import models
from django.conf import settings
from user_system.models import UserPersonalized
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


# Create your models here.

# execute this command
# shell: exec(open('user_system/groups_and_permissions.py').read())
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
    checks = models.ManyToManyField(UserPersonalized, related_name='checks')
    rates = models.ManyToManyField(UserPersonalized, through='Rate', related_name='rates')


    # function to obtain the number of rates of a publication
    def rate_count(self):
        return self.rates.count()

    # function to obtain the average rate of a publication
    def rate_average(self):
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
        n_rate = self.rate_count()
        avg_rate = self.rate_average()
        return n_rate * (avg_rate ** avg_rate)

class Rate(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    user = models.ForeignKey(UserPersonalized, on_delete=models.CASCADE)
    rate_value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)]) # the rate will be in th range of 1-5


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
