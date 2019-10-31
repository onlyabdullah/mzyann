from django.utils.translation import gettext_lazy as _
from django import forms

from professionals.models import (
    Area, Job
)

class SearchForm(forms.Form):
    area = forms.ModelChoiceField(empty_label="Choose", queryset=Area.objects.all())
    job = forms.ModelChoiceField(empty_label="Choose", queryset=Job.objects.all())
    item = forms.ChoiceField(choices=((('', 'Choose'),)))
    name = forms.CharField(max_length=150, required=False)


class FilterForm(forms.Form):
    ORDER_BY_CHOICES = (
        ('-ratings__average', _('Rating')),
        ('user__user_menu__menu_items__price', _('Price: Low to High')),
        ('-user__user_menu__menu_items__price', _('Price: High to Low'))
    )

    price_from = forms.IntegerField(widget=forms.HiddenInput(), min_value=0, max_value=10000, required=False)
    price_to = forms.IntegerField(widget=forms.HiddenInput(), min_value=0, max_value=10000, required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY_CHOICES, required=False)

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        price_from = cleaned_data.get('price_form')
        price_to = cleaned_data.get('price_to')
        
        if price_from and price_to:
            if price_from < 0 or price_to < 0:
                raise forms.ValidationError(_('Value should be positive integer'))

            if price_from > price_to:
                raise forms.ValidationError(_('Value of price from should be less than price to'))