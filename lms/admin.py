from django.contrib import admin
from .models import Judul, Kursus, Modul

# Use @admin.register() decorator to register app to django admin
@admin.register(Judul)
class JudulAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepoulated_fields = {'slug': ('title',)}

class ModulInline(admin.StackedInline):
    model = Modul

@admin.register(Kursus)
class KursusAdmin(admin.ModelAdmin):
    list_display = ['title', 'judul', 'created']
    list_filter = ['created', 'judul']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModulInline]
