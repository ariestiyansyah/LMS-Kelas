from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from .models import Kursus

class XmanMixin(object):
    def get_queryset(self):
        qs = super(XmanMixin, self).get_queryset()
        return qs.filter(xman=self.request.user)

class XmanEditMixin(object):
    def form_valid(self, form):
        form.instance.xman = self.request.user
        return super(XmanEditMixin, self).form_valid(form)

class XmanKursusMixin(XmanMixin, LoginRequiredMixin):
    model = Kursus
    fields = ['judul', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_kursus_list')

class XmanKursusEditMixin(XmanKursusMixin, XmanEditMixin):
    fields = ['judul', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_kursus_list')
    template_name = 'lms/manage/kursus/form.html'

class ManageKursusListView(XmanKursusMixin, ListView):
    template_name = 'lms/manage/kursus/list.html'

class KursusCreateView(PermissionRequiredMixin, XmanKursusEditMixin, CreateView):
    permission_required = 'courses.addp_course'

class KursusUpdateView(PermissionRequiredMixin, XmanKursusEditMixin, UpdateView):
    permission_required = 'courses.change_course'
    template_name = 'lms/manage/kursus/form.html'

class KursusDeleteView(PermissionRequiredMixin, XmanKursusEditMixin, DeleteView):
    template_name = 'lms/manage/kursus/delete.html'
    success_url = reverse_lazy('manage_kursus_list')
    permission_required = 'courses.delete_course'
