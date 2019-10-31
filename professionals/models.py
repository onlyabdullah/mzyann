import hashlib
from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

import cloudinary
from cloudinary.models import CloudinaryField
from star_ratings.models import Rating

from accounts.models import User
from accounts import validators


class AcceptedManager(models.Manager):
    def get_queryset(self):
        return super(AcceptedManager, self).get_queryset().filter(status='accepted')


class Profile(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected'))
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = CloudinaryField('image')
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='job_users')
    about = models.TextField(_('About'), max_length=255)
    area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='area_users')
    phone_number = models.CharField(validators=[validators.phone_number_validator], max_length=11, blank=True)
    call_time_from = models.TimeField(blank=True, null=True)
    call_time_to = models.TimeField(blank=True, null=True)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='pending')
    features = models.ManyToManyField('Feature', related_name='feature_users', blank=True)
    ratings = GenericRelation(Rating)
    slug = models.SlugField(max_length=255)
    meta_description = models.TextField(blank=True, null=True)

    objects = models.Manager()
    accepted = AcceptedManager()

    class Meta:
        db_table = 'professionals_profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self):
        return "{email}'s Profile".format(email=self.user.email)


class Area(models.Model):
    name = models.CharField(_('Area'), max_length=50)
    name_ar = models.CharField(_('Area ar'), max_length=50)


    class Meta:
        db_table = 'professionals_area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

    def __str__(self):
        return "{name}".format(name=self.name)


class Job(models.Model):
    name = models.CharField(_('Job'), max_length=50)
    name_ar = models.CharField(_('Job ar'), max_length=50)

    class Meta:
        db_table = 'professionals_job'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return "{name}".format(name=self.name)


class Feature(models.Model):
    name = models.CharField(_('Feature'), max_length=50)
    name_ar = models.CharField(_('Feature ar'), max_length=50)

    class Meta:
        db_table = 'professionals_feature'
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'
    
    def __str__(self):
        return "{name}".format(name=self.name)


class Item(models.Model):
    name = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='job_items')

    class Meta:
        db_table = 'professionals_item'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return "{name}".format(name=self.name)


class Menu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_menu')

    class Meta:
        db_table = 'professionals_menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return "{email}'s Menu".format(email=self.user)


class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='menu_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='item_menu_items')
    price = models.IntegerField()

    class Meta:
        db_table = 'professionals_menu_item'
        verbose_name = 'MenuItem'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return "{item}'s ".format(item=self.item)


class SocialWebsite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_social_websites')
    facebook = models.URLField(_('Facebook'), validators=[validators.facebook_validator], blank=True, null=True)
    twitter = models.URLField(_('Twitter'), validators=[validators.twitter_validator], blank=True, null=True)
    instagram = models.URLField(_('Instagram'), validators=[validators.instagram_validator], blank=True, null=True)
    youtube = models.URLField(_('Youtube'), validators=[validators.youtube_validator], blank=True, null=True)

    class Meta:
        db_table = 'professionals_social_website'
        verbose_name = 'Social Website'
        verbose_name_plural = 'Social Websites'
    
    def __str__(self):
        return "{email}'s Social Website".format(email=self.user.email)


@receiver(pre_delete, sender=Profile)
def profile_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.profile_picture.public_id)
    instance.user.user_menu.delete()
    instance.user.user_album.delete()
    instance.user.user_social_websites.delete()

    if instance.user.groups.filter(name='professional').exists():
        user = instance.user
        group = Group.objects.get(name='professional')
        user.groups.remove(group)

@receiver(pre_save, sender=Profile)
def profile_save(sender, instance, **kwargs):
    if not instance.slug:
        slug_hash = hashlib.md5()
        slug_hash.update(str(datetime.now()).encode('utf-8'))
        instance.slug = '{0}-{1}-{2}-{3}'.format(instance.job, instance.user.first_name, instance.user.last_name, slug_hash.hexdigest()[:15]).lower()[:255]

    if instance.status == 'accepted' and not instance.user.groups.filter(name='professional').exists():
        user = instance.user
        group = Group.objects.get(name='professional')
        user.groups.add(group)
    elif instance.status != 'accepted':
        user = instance.user
        group = Group.objects.get(name='professional')
        user.groups.remove(group)
