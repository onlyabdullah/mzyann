from django.views.generic import TemplateView


class PrivacyTemplateView(TemplateView):
    template_name = 'privacy_policy/privacy_policy.html'
