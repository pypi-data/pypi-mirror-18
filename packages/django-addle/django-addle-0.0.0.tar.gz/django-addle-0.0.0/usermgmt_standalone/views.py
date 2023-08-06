from django.contrib.auth import (
    authenticate,
    login,
)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.views.generic import FormView

from .forms import RegisterForm


class Register(FormView):
    """View to register a new user."""
    template_name = 'registration/new.html'
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        login(self.request, new_user)
        return super(Register, self).form_valid(form)

    def get_success_url(self):
        return self.request.POST.get(
            'next', self.request.GET.get(
                'next', reverse('usermgmt_standalone:view_user', kwargs={
                    'username': self.request.user.username,
                })))

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


def view_user(request, username=None):
    user = get_object_or_404(User, username=username)
    return render(request, 'view_profile.html', {
        'title': user.username,
        'profile': user,
    })
