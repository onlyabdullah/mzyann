from django.urls import path

from . import views

urlpatterns = [
    path(
        'portfolios/album/create/',
        views.AlbumCreateView.as_view(),
        name='portfolios_create_album'
    ),
    path(
        'portfolios/album/update/<int:pk>/',
        views.AlbumUpdateView.as_view(),
        name='portfolios_upload_images'
    ),
    path(
        'portfolios/image/delete/<int:pk>/',
        views.ImageDeleteView.as_view(),
        name='portfolios_image_delete'
    ),
    path(
        'portfolios/image/update/<int:pk>/',
        views.ImageUpdateView.as_view(),
        name='portfolios_image_update'
    )
]
