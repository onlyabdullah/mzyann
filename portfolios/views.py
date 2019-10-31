import json
import base64

from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, ListView, View, DeleteView, UpdateView
)

from django.forms.models import modelform_factory

from .models import (
    Album, Image
)
from .forms import ImageCreateForm

from professionals.mixins import GroupRequiredMixin


class AlbumCreateView(View):
    def get_form(self, model, fields):
        return modelform_factory(model=model, fields=fields)

    def post(self, request):
        if not request.session.get('become_professional_portfolio'):
            request.session['become_professional_portfolio'] = []

        if request.is_ajax():
            image_form = ImageCreateForm(request.POST, request.FILES)
            if image_form.is_valid():
                if len(request.session['become_professional_portfolio']) < 5:
                    with open(image_form.cleaned_data['image'], 'rb') as image_file:
                        image_file = base64.b64encode(image_file.read())
                        payload = {'image_file': image_file}
                        request.session['become_professional_portfolio'].append(json.dumps(payload))
                    data = {'is_valid': True, 'url': image_file}
                else:
                    data = {'is_valid': False, 'limit_exceeded': True}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)


class AlbumUpdateView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = [u'professional']

    def get_form(self, model, fields):
        return modelform_factory(model=model, fields=fields)

    def get(self, request, pk):
        images_list = Image.objects.filter(album__pk=pk)

        images = []
        for image in images_list:
            image_form = self.get_form(model=Image, fields=('show_to',))(instance=image)
            images.append({'image': image, 'form': image_form})

        return render(
            self.request,
            'portfolios/update_portfolio.html',
            {
                'images': images,
                'pk': pk,
            }
        )

    def post(self, request, pk):
        album = Album.objects.get(pk=pk)

        if request.is_ajax():
            image_form = self.get_form(model=Image, fields=('image',))(request.POST, request.FILES)
            if image_form.is_valid():
                if len(album.album_images.all()) < 20:
                    image = image_form.save(commit=False)
                    image.album = album
                    image.save()
                    data = {'is_valid': True, 'url': image.image.url}
                else:
                    data = {'is_valid': False, 'limit_exceeded': True}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)


class ImageDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Image
    group_required = [u'professional']

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('mzyann_home_page')
        return super(ImageDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolios_upload_images', kwargs={'pk': self.object.album.pk})


class ImageUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Image
    group_required = [u'professional']
    fields = ('show_to',)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('mzyann_home_page')
        return super(ImageUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolios_upload_images', kwargs={'pk': self.object.album.pk})
