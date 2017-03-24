from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.apps import apps
from django.forms.models import modelform_factory
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course, Module, Content
from .forms import ModuleFormSet

class XmanMixin(object):
    def get_queryset(self):
        qs = super(XmanMixin, self).get_queryset()
        return qs.filter(xman=self.request.user)

class XmanEditMixin(object):
    def form_valid(self, form):
        form.instance.xman = self.request.user
        return super(XmanEditMixin, self).form_valid(form)

class XmanCourseMixin(XmanMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class XmanCourseEditMixin(XmanCourseMixin, XmanEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'cms/manage/course/form.html'

class ManageCourseListView(XmanCourseMixin, ListView):
    template_name = 'cms/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin, XmanCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin, XmanCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'
    template_name = 'cms/manage/course/form.html'

class CourseDeleteView(PermissionRequiredMixin, XmanCourseEditMixin, DeleteView):
    template_name = 'cms/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'cms/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        xman=request.user)
        return super(CourseModuleUpdateView,
                     self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'format': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'cms/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['teks', 'video', 'gambar', 'file']:
            return apps.get_model(app_label='cms', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['xman','order','created','updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__xman=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, xman=request.user)

        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    # get() and pos() method for ContentCreateUpdateView

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
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
                Content.objects.create(module=self.module,
                                      item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form, 
                                        'object': self.obj})

# Delete Content
class ContentDeleteView(View):
    def post(self, request, id):
        Content = get_object_or_404(Content, id=id, module__course__xman=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

# List Module Content
class ModuleContentListView(TemplateResponseMixin, View):
    template_name  = 'cms/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                  id=module_id,
                                  course__xman=request.user)
        return self.render_to_response({'module': module})
