from django.db import models
from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

class Judul(models.Model):
    title = models.CharField(max_length=100) # Title of the course
    slug = models.SlugField(max_length=100, unique=True) # slug of the course

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Kursus(models.Model):
    xman = models.ForeignKey(User, related_name='courses_created') # Instructor of the course
    judul = models.ForeignKey(Judul, related_name='courses') # course subject
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    overview = models.TextField() # Set overview column
    created = models.DateTimeField(auto_now_add=True) # when the course was created, using auto_now_add=True to automatically set by Django

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Modul(models.Model):
    kursus = models.ForeignKey(Kursus, related_name='modules')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['kursus'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Konten(models.Model):
    module = models.ForeignKey(Modul, related_name='contents')  # Define ForeignKey to Modul model
    content_type = models.ForeignKey(ContentType,
            limit_choices_to={'model__in':('teks',
                'video',
                'gambar',
                'file')})
    object_id = models.PositiveIntegerField() # Store pimary key
    item = GenericForeignKey('content_type', 'object_id') # Generic relation to associate objects from different models
    order = OrderField(blank=True, for_fields=['modul'])

    class Meta:
        ordering = ['order']

class KontenBase(models.Model):
    xman = models.ForeignKey(User, related_name='%(class)s_related')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Teks(KontenBase):
    konten = models.TextField()

class File(KontenBase):
    file = models.FileField(upload_to='files')

class Gambar(KontenBase):
    file = models.FileField(upload_to='images')

class Video(KontenBase):
    url = models.URLField()
