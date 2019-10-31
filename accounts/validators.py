import os
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

def name_validator(name):
    if not name.isalpha():
        raise ValidationError(_('Name should contain letters only.'))
    return name

def link_validator(link, website_name):
    if not website_name in link.replace('https://', '').split('.'):
        raise ValidationError(_('Should be a valid '+website_name+' link.'))
    return link

def facebook_validator(link):
    return link_validator(link, 'facebook')

def twitter_validator(link):
    return link_validator(link, 'twitter')


def instagram_validator(link):
    return link_validator(link, 'instagram')


def youtube_validator(link):
    return link_validator(link, 'youtube')


def phone_number_validator(phone_number):
    if len(phone_number) != 11 or not phone_number.isdigit():
        raise ValidationError(_('Phone number should be 11 digit'))

    if not phone_number.startswith('012') and not phone_number.startswith('010') and\
        not phone_number.startswith('011') and not phone_number.startswith('015'):
        raise ValidationError(_('Phone number should starts with 010, 011, 012 or 015'))
    return phone_number 
