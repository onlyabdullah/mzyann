from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'gender',
        'date_joined',
        'last_login'
    )
    list_filter = ('gender', 'date_joined', 'last_login')
    search_fields = ['first_name', 'last_name', 'email']
