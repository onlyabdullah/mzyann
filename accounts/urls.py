# Django General Imports
from django.urls import path

# Accounts App Views
from . import views

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(),
        name='account_login'
    ),
]
