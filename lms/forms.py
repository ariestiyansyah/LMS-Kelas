from django import forms
from django.forms.models import inlineformset_factory
from .models import Kursus, Modul

ModulFormSet = inlineformset_factory(Kursus, Modul, fields=['title','description'], extra=2, can_delete=True)