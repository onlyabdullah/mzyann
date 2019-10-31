from django.conf import settings
from django.utils import translation
from django.http.response import JsonResponse, HttpResponseRedirect
from django.views.generic import  (
    TemplateView, ListView
)

from django.db.models.query_utils import Q
from professionals.models import (
    Profile, Item
)

from .forms import SearchForm, FilterForm


class HomePageView(TemplateView):
    template_name = 'mzyann_app/home_page.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            job = self.request.GET.get('job')
            item = self.request.GET.get('item')
            item_options = Item.objects.filter(job=job)
            if item_options:
                item_options = [(e.pk, e.name) for e in item_options]
                data = {'is_valid': True, 'item_options': item_options, 'selected_item': item}
            else:
                data = {'is_valid': False}
            return JsonResponse(data=data)
        return super(HomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['form'] = SearchForm
        return context


class SearchResultView(ListView):
    model = Profile
    template_name = 'mzyann_app/search_result.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(SearchResultView, self).get_queryset()
        area = self.request.GET.get('area')
        job = self.request.GET.get('job')
        item = self.request.GET.get('item')
        name = self.request.GET.get('name')
        price_from =self.request.GET.get('price_from')
        price_to =self.request.GET.get('price_to')
        order_by = self.request.GET.get('order_by')

        if not order_by:
            order_by = 'ratings__average'
        
        if not price_from and not price_to:
            price_from = 0
            price_to = 10000

        if name:
            queryset = Profile.accepted.filter(
                Q(area=area, job=job, user__user_menu__menu_items__item__in=item, user__first_name__icontains=name, user__user_menu__menu_items__price__gte=price_from, user__user_menu__menu_items__price__lte=price_to) |
                Q(area=area, job=job, user__user_menu__menu_items__item__in=item, user__last_name__icontains=name, user__user_menu__menu_items__price__gte=price_from, user__user_menu__menu_items__price__lte=price_to)).order_by(order_by)
            if len(name.split()) > 1:
                queryset = Profile.accepted.filter(
                    Q(area=area, job=job, user__user_menu__menu_items__item__in=item, user__user_menu__menu_items__price__gte=price_from, user__user_menu__menu_items__price__lte=price_to, user__first_name__icontains=name.split()[0], user__last_name__icontains=name.split()[1])).order_by(order_by)
        else:
            queryset = Profile.accepted.filter(Q(area=area, job=job, user__user_menu__menu_items__item__in=item, user__user_menu__menu_items__price__gte=price_from, user__user_menu__menu_items__price__lte=price_to)).order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(data=self.request.GET)
        context['filter_form'] = FilterForm(data=self.request.GET)
        object_list = []
        for profile in self.object_list:
            item = profile.user.user_menu.menu_items.get(item=self.request.GET.get('item'))
            object_list.append((profile, item))
        context['object_list'] = object_list
        return context


# def change_language(request):
#     lang_code = request.GET.get('lang_code')

#     response = HttpResponseRedirect(request.GET.get('return_url'))
#     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#     translation.activate(lang_code)
#     return response
