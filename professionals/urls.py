# Django General imports
from django.urls import path

# professionals App Views
from . import views

urlpatterns = [
    path(
        'become-professional/',
        views.BecomeProfessionalRequestView.as_view(),
        name='professionals_become_professional_request'
    ),
    path(
        'profile/<str:slug>/',
        views.ProfileView.as_view(),
        name='professionals_profile'
    ),
    path(
        'update/<str:model_name>/<int:pk>/',
        views.ProfileObjectsUpdateView.as_view(),
        name='professionals_update_object'
    ),
    path(
        'menu-item/create/',
        views.MenuItemCreateView.as_view(),
        name='professionals_create_menu_item'
    ),
    path(
        'menu-item/update/<int:pk>/',
        views.MenuItemUpdateView.as_view(),
        name='professionals_update_menu_item'
    ),
    path(
        'menu-item/delete/<int:pk>/',
        views.MenuItemDeleteView.as_view(),
        name='professionals_delete_menu_item'
    )
]

