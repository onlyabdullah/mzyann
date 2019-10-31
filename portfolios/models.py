from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import cloudinary
from cloudinary.models import CloudinaryField

from accounts.models import User

from accounts.validators import name_validator

class Album(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_album')

    class Meta:
        db_table = 'portfolios_album'
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'
    
    def __str__(self):
        return "{email}'s Album".format(email=self.user.email)


class Image(models.Model):
    SHOW_TO_CHOICES = (
        ('both', _('Both')),
        ('male', _('Male')),
        ('female', _('Female')),
    )

    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='album_images')
    image = CloudinaryField('image')
    show_to = models.CharField(max_length=30, choices=SHOW_TO_CHOICES, default='both')

    class Meta:
        db_table = 'portfolios_image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return "{album}'s Image".format(album=self.album.user)


@receiver(pre_delete, sender=Image)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)
