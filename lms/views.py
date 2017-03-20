from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Kursus

class XmanMixin(object):
    def get_queryset(self):
        qs = super(XmanMixin, self).get_queryset()
        return qs.filter(xman=self.request.user)

class XmanEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(XmanEditMixin, self).form_valid(form)

class XmanKursusMixin(XmanMixin):
    model = Kursus

class XmanKursusEditMixin(XmanKursusMixin, XmanEditMixin):
    fields = ['judul', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'lms/manage/kursus/form.html'

class ManageKursusListView(XmanKursusMixin, ListView):
    template_name = 'lms/manage/kursus/list.html'

class KursusCreateView(XmanKursusEditMixin, CreateView):
    pass

class KursusUpdateView(XmanKursusEditMixin, UpdateView):
    pass

class KursusDeleteView(XmanKursusEditMixin, DeleteView):
    template_name = 'lms/manage/kursus/delete.html'
    success_url = reverse_lazy('manage_course_list)

#    def get_queryset(self):
#        qs = super(ManageKursusListView, self).get_queryset()
#        return qs.filter(xman=self.request.user)
