from django.db import models

# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    


class Field(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=False)
    next = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True

class FieldText(Field):
    text = models.CharField(max_length=500)

class FieldImage(Field):
    image = models.ImageField(upload_to='imagenes/')

class FieldVideo(Field):
    video = models.FileField(upload_to='videos/')


