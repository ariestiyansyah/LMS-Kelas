from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps
from django.forms.models import modelform_factory
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from .models import Kursus, Modul, Konten
from .forms import ModulFormSet

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

class KursusModulUpdateView(TemplateResponseMixin, View):
    template_name = 'lms/manage/module/formset.html'
    kursus = None

    def get_formset(self, data=None):
        return ModulFormSet(instance=self.kursus, data=data)

    def dispatch(self, request, pk):
        self.kursus = get_object_or_404(Kursus,
                                        id=pk,
                                        xman=request.user)
        return super(KursusModulUpdateView,
                     self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'kursus': self.kursus,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_kursus_list')
        return self.render_to_response({'kursus': self.kursus,
                                        'format': formser})


class KontenCreateUpdateView(TemplateResponseMixin, View):
    modul = None
    model = None
    obj = None
    template_name = 'lms/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['teks', 'video', 'gambar', 'file']:
            return apps.get_model(app_label='lms', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['xman','order','created','updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, modul_id, model_name, id=None):
        self.modul = get_object_or_404(Modul, id=modul_id, kursus__xman=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, xman=request.user)

        return super(KontenCreateUpdateView, self).dispatch(request, modul_id, model_name, id)

    # get() and pos() method for KontenCreateUpdateView

    def get(self, request, modul_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, modul_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.xman = request.user
            obj.save ()
            if not id:
            # New Content Here
                Konten.objects.create(modul=self.modul,
                                      item=obj)
            return redirect('modul_konten_list', self.modul.id)

        return self.render_to_response({'form': form, 
                                        'object': self.obj})

# Delete Content
class KontenDeleteView(View):
    def post(self, request, id):
        konten = get_object_or_404(Konten, id=id, modul__kursus__xman=request.user)
        modul = konten.modul
        konten.item.delete()
        konten.delete()
        return redirect('modul_konten_list', modul.id)

# List Module Content
class ModulKontenListView(TemplateResponseMixin, View):
    template_name  = 'lms/manage/module/content_list.html'

    def get(self, request, modul_id):
        modul = get_object_or_404(Modul,
                                  id=modul_id,
                                  kursus__xman=request.user)
        retrun self.render_to_response({'modul': modul})
