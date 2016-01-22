import json
import requests

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView
from django.utils.translation import ugettext as _
from django.conf import settings

from candidates.models.address import check_address
from elections.models import Election
from .mixins import ContributorsMixin

from ..forms import AddressForm


class GeoLocatorView(View):
    def get(self, request, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']

        for election in Election.objects.current().prefetch_related('area_types'):
            area_types = election.area_types.values_list('name', flat=True)

        mapit_lookup_url = '{base_url}point/4326/{lon},{lat}'.format(
            base_url=settings.MAPIT_BASE_URL,
            lon=longitude,
            lat=latitude,
        )

        mapit_lookup_url += '?type=' + ','.join(area_types)
        mapit_lookup_url += '&generation={0}'.format(election.area_generation)
        mapit_result = requests.get(mapit_lookup_url)
        mapit_json = mapit_result.json()
        if 'error' in mapit_json:
            message = _(u"The area lookup returned an error: '{error}'")
            return HttpResponse(
                json.dumps({'error': message}),
                content_type='application/json',
            )

        if len(mapit_json) == 0:
            message = _(u"Your location does not seem to be covered by this site")
            return HttpResponse(
                json.dumps({'error': message}),
                content_type='application/json',
            )

        ids_and_areas = [
            "{0}-{1}".format(area['type'], area_id)
            for area_id, area in mapit_json.items()
        ]

        return HttpResponseRedirect(
            reverse('areas-view', kwargs={
                'type_and_area_ids': ','.join(ids_and_areas)
            })
        )


class AddressFinderView(ContributorsMixin, FormView):
    template_name = 'candidates/frontpage.html'
    form_class = AddressForm
    country = None

    @method_decorator(cache_control(max_age=(60 * 10)))
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddressFinderView, self).dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.country, **self.get_form_kwargs())

    def form_valid(self, form):
        form.cleaned_data['address']
        resolved_address = check_address(
            form.cleaned_data['address'],
            country=self.country,
        )
        return HttpResponseRedirect(
            reverse('areas-view', kwargs=resolved_address)
        )

    def get_context_data(self, **kwargs):
        context = super(AddressFinderView, self).get_context_data(**kwargs)
        context['top_users'] = self.get_leaderboards()[1]['rows'][:8]
        context['recent_actions'] = self.get_recent_changes_queryset()[:5]
        context['election_data'] = Election.objects.current().by_date().last()
        return context
