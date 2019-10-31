from django.shortcuts import reverse, redirect
from django.views.generic import UpdateView, TemplateView

from .models import User


class LoginView(TemplateView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('mzyann_home_page')
        return super(LoginView, self).dispatch(request, *args, **kwargs)
