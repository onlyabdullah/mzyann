import os
# Django General Imports
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# Django Forms
from django.forms.models import (
    modelform_factory
)
from django.shortcuts import (
    Http404, get_object_or_404, redirect, render, reverse
)
from django.template.response import TemplateResponse
from django.http import  (
    HttpResponse, Http404, HttpResponseServerError
)
# Django Generic Views
from django.views.generic import (
    CreateView, DeleteView, DetailView, FormView, TemplateView, UpdateView, View
)
# Django Formtools Views
from formtools.wizard.views import SessionWizardView
# Accounts app models
from accounts.models import User
# Professional app forms
from .forms import (
    MenuItemCreateUpdateForm, ProfileInfoForm, PortfolioForm, SocialWebsitesForm
)
# Professionals app Mixins
from .mixins import GroupRequiredMixin
# Professionals app models
from .models import (
    Item, MenuItem, Profile, SocialWebsite, Menu
)
# 
from portfolios.models import (
    Album, Image
)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "professionals/profile.html"

    def dispatch(self, request, slug):
        profile = Profile.objects.filter(user=request.user).first()
        if profile and profile.status == 'pending':
            raise Http404
        return super(ProfileView, self).dispatch(request, slug)


class BecomeProfessionalRequestView(LoginRequiredMixin, SessionWizardView):
    template_name = 'professionals/become_professional_request.html'
    form_list = [ProfileInfoForm, PortfolioForm, SocialWebsitesForm]
    file_storage = FileSystemStorage(os.path.join(settings.MEDIA_ROOT, 'temp'))

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            if profile.status == 'accepted':
                return TemplateResponse(request, template='professionals/become_professional_already_professional.html')
            elif profile.status == 'pending':
                return TemplateResponse(request, template='professionals/become_professional_done.html')
        return super(BecomeProfessionalRequestView, self).get(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        user = self.request.user
        form_list = list(form_list)
        profile_info_form = form_list[0]
        portfolio_form = form_list[1]
        social_websites_form = form_list[2]

        profile_picture = profile_info_form.cleaned_data.get('profile_picture')
        about = profile_info_form.cleaned_data.get('about')
        phone_number = profile_info_form.cleaned_data.get('phone_number')
        job = profile_info_form.cleaned_data.get('job')
        area = profile_info_form.cleaned_data.get('area')

        facebook = social_websites_form.cleaned_data.get('facebook')
        instagram = social_websites_form.cleaned_data.get('instagram')
        twitter = social_websites_form.cleaned_data.get('twitter')
        youtube = social_websites_form.cleaned_data.get('youtube')
        
        try:
            profile = Profile(
                user=user,
                profile_picture=profile_picture,
                about=about,
                phone_number=phone_number,
                job=job,
                area=area
            )
            profile.save()

            album = Album.objects.create(user=user)
            for i in range(5):
                image = Image(
                    album=album,
                    image=portfolio_form.cleaned_data.get('image_'+str(i))
                )
                image.save()

            social_websites = SocialWebsite(
                user=user,
                facebook=facebook,
                instagram=instagram,
                twitter=twitter,
                youtube=youtube
            )
            social_websites.save()

            menu = Menu(user=user)
            menu.save()
            return TemplateResponse(self.request, template='professionals/become_professional_done.html')
        except:
            return HttpResponseServerError('Please, try again.')


class ProfileObjectsUpdateView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    model = None
    obj = None
    group_required = [u'professional']

    def get_model(self, model_name):
        return apps.get_model(app_label='professionals', model_name=model_name)

    def dispatch(self, request, model_name, pk):
        if model_name in ['socialwebsite', 'profile', 'menu']:
            self.model = self.get_model(model_name)
            if model_name == 'socialwebsite':
                self.template_name = 'professionals/update_social_website.html'
            elif model_name == 'profile':
                self.template_name = 'professionals/update_profile.html'
            elif model_name == 'menu':
                self.template_name = 'professionals/update_menu.html'

            obj = get_object_or_404(
                self.model,
                pk=pk
            )
            if obj.user == request.user:
                if model_name == 'profile' and obj.status == 'pending':
                    raise Http404
                self.obj = obj
            else:
                return redirect(reverse('mzyann_home_page'))
        else:
            raise Http404
        return super(ProfileObjectsUpdateView, self).dispatch(request, model_name, pk)

    def get_form(self, model, *args, **kwargs):
        model_name = model.__name__.lower()

        exclude = None

        if model_name == 'profile':
            exclude = ('user', 'status', 'slug', 'meta_title', 'meta_description', 'featrues', 'job')
        elif model_name == 'pricelist':
            exclude = ('user',)
        elif model_name == 'socialwebsite':
            exclude = ('user',)

        form = modelform_factory(model=model, exclude=exclude, *args, **kwargs)
        return form

    def get(self, request, model_name, pk=None):
        if model_name != 'menu':
            form = self.get_form(model=self.model)(instance=self.obj)
            context = {
                'form': form,
            }
        else:
            context = {
                'menu_items': self.obj.menu_items.all()
            }

        if model_name == 'profile':
            fields = ('first_name', 'last_name',)
            account_form = self.get_form(model=User, fields=fields)(instance=self.obj.user)
            context['account_form'] = account_form

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request, model_name, pk=None):
        form = self.get_form(model=self.model)(request.POST, request.FILES, instance=self.obj)
        context = {'form': form}

        if model_name == 'profile':
            fields = ('first_name', 'last_name',)
            account_form = self.get_form(model=User, fields=fields)(request.POST, instance=self.obj.user)
            context['account_form'] = account_form

        if form.is_valid():
            obj = form.save(commit=False)
    
            if not pk:
                obj.user = request.user

            if model_name == 'profile':
                if account_form.is_valid():
                    account_form.save()

            obj.save()

            return redirect('professionals_update_object', model_name=model_name, pk=self.obj.pk)
        
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )


class MenuItemCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = MenuItem
    template_name = 'professionals/create_update_menu_item.html'
    form_class = MenuItemCreateUpdateForm
    group_required = [u'professional']

    def get_form(self, form_class=None):
        if form_class is None:
                form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.menu = self.request.user.user_menu
        self.object.save()
        return super(MenuItemCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('professionals_update_object', kwargs={'model_name': 'menu', 'pk': self.request.user.user_menu.pk})


class MenuItemUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = MenuItem
    template_name = 'professionals/create_update_menu_item.html'
    fields = ('price',)
    group_required = [u'professional']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('mzyann_home_page')
        return super(MenuItemUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MenuItemUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def get_success_url(self):
        return reverse('professionals_update_object', kwargs={'model_name': 'menu', 'pk': self.request.user.user_menu.pk})


class MenuItemDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = MenuItem
    group_required = [u'professional']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('mzyann_home_page')
        return super(MenuItemDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('professionals_update_object', kwargs={'model_name': 'menu', 'pk': self.request.user.user_menu.pk})
