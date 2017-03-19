from django.db import models
from django.contrib.auth.models import User 

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

    def __str__(self):
        return self.title
