from django.contrib import admin

from .models import (
    Profile, Menu, Item, SocialWebsite, MenuItem, Area, Feature, Job
)

admin.site.register(Menu)
admin.site.register(MenuItem)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'job',
        'area',
        'phone_number',
        'status'
    )
    list_filter = ('job', 'area', 'status', 'features')
    search_fields = ['user', 'area', 'status', 'features']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'job')
    list_filter = ('job',)
    search_fields = ['name', 'job']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(SocialWebsite)
class SocialWebsiteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'facebook',
        'twitter',
        'instagram',
        'youtube'
    )
    search_fields = ['user']
