from django.db import models
from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

# Subject Model
class Subject(models.Model):
    title = models.CharField(max_length=100) # Title of the course
    slug = models.SlugField(max_length=100, unique=True) # slug of the course

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

# Course Model
class Course(models.Model):
    xman = models.ForeignKey(User, related_name='courses_created') # Instructor of the course
    subject = models.ForeignKey(Subject, related_name='courses') # course subject
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    overview = models.TextField() # Set overview column
    created = models.DateTimeField(auto_now_add=True) # when the course was created, using auto_now_add=True to automatically set by Django

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

# Module Model
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

# Content Model
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents')  # Define ForeignKey to Module model
    content_type = models.ForeignKey(ContentType,
            limit_choices_to={'model__in':('teks',
                'video',
                'gambar',
                'file')})
    object_id = models.PositiveIntegerField() # Store pimary key
    item = GenericForeignKey('content_type', 'object_id') # Generic relation to associate objects from different models
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ContentBase(models.Model):
    xman = models.ForeignKey(User, related_name='%(class)s_related')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Teks(ContentBase):
    content = models.TextField()

class File(ContentBase):
    file = models.FileField(upload_to='files')

class Gambar(ContentBase):
    file = models.FileField(upload_to='images')

class Video(ContentBase):
    url = models.URLField()
