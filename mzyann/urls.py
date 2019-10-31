from django.contrib import admin
from django.urls import path
from django.conf.urls import include, handler400, handler403, handler404, handler500
from django.conf import settings

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from allauth.account.urls import urlpatterns as allauth_account_urls
from allauth.socialaccount.urls import urlpatterns as allauth_socialaccount_patterns

from common import views as errors_views

allauth_account_patterns = (
    [
        allauth_account_urls[2],
        allauth_account_urls[5],
        allauth_account_urls[7],
        allauth_account_urls[8]
    ]
)

allauth_socialaccount_patterns = (
    [
        allauth_socialaccount_patterns[0],
        allauth_socialaccount_patterns[1],
        allauth_socialaccount_patterns[2]
    ]
)

urlpatterns = [
    path('accounts/', include(allauth_account_patterns)),
    path('accounts/social/', include(allauth_socialaccount_patterns)),
    path('accounts/social/', include('allauth.socialaccount.providers.facebook.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('professionals.urls')),
    path('accounts/', include('portfolios.urls')),
    path('', include('privacy_policy.urls')),
    path('', include('mzyann_app.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings'))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('admin/', admin.site.urls),
