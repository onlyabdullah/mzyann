from django.shortcuts import redirect, reverse
from django.contrib.auth.models import Group

from professionals.models import (
    Profile, SocialWebsite, Menu
)
from portfolios.models import (
    Album, Image
)

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        user.first_name = form.cleaned_data.get('first_name').title()
        user.last_name = form.cleaned_data.get('last_name').title()
        user.gender = form.cleaned_data.get('gender')
        user.save()

    def get_login_redirect_url(self, request):
        return '/'
