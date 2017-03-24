from django.core.urlresolvers import reverse_lazy
from django.view.generic.edit import CreateView 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

class LmsRegistrationView(CreateView):
    template_name = 'lms/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valide(self, form):
        result = super(LmsRegistrationView,
                       self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password'])
        login(self.request, user)
        return result