from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='mzyann_home_page'
    ),
    path(
        'search/',
        views.SearchResultView.as_view(),
        name='mzyann_search'
    ),
    # path(
    #     'change-langauge/',
    #     views.change_language,
    #     name='mzyann_change_language'
    # )
]
