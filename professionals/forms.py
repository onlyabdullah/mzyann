from django import forms

from django.db.models import Q

# Models
from .models import Menu, MenuItem, Item, Job, Area, Feature

# Accounts App Name Validator
from accounts import validators


class MenuItemCreateUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MenuItemCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['item'] = forms.ModelChoiceField(
            empty_label='',
            queryset=Item.objects.filter(
                ~Q(item_menu_items__in=self.user.user_menu.menu_items.all()),
                job=self.user.user_profile.job
            )
        )

    class Meta:
        model = MenuItem
        fields = ('item', 'price',)


class ProfileInfoForm(forms.Form):
    profile_picture = forms.ImageField()
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':15}), max_length=255)
    phone_number = forms.CharField(max_length=11, validators=[validators.phone_number_validator])
    job = forms.ModelChoiceField(queryset=Job.objects.all(), empty_label="")
    area = forms.ModelChoiceField(queryset=Area.objects.all(), empty_label="")


class PortfolioForm(forms.Form):
    image_0 = forms.ImageField()
    image_1 = forms.ImageField()
    image_2 = forms.ImageField()
    image_3 = forms.ImageField()
    image_4 = forms.ImageField()


class SocialWebsitesForm(forms.Form):
    facebook = forms.URLField(required=False, validators=[validators.facebook_validator])
    twitter = forms.URLField(required=False, validators=[validators.twitter_validator])
    instagram = forms.URLField(required=False, validators=[validators.instagram_validator])
    youtube = forms.URLField(required=False, validators=[validators.youtube_validator])
