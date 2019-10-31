from django import forms

from .models import Image


class ImageCreateForm(forms.Form):
    image = forms.ImageField()
