# Django modules
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site

# App Models
from .models import ItineraryModel, TimeModel, ViableTourTimeModel, HomeVisitModel
from .serializers import ItinerarySerializer, ViableTourTimeSerializer
from .helpers.send_emails import send_new_itinerary_marketplace_email, send_new_itinerary_referred_email

# Cocoon Modules
from cocoon.userAuth.models import UserProfile, MyUser
from cocoon.survey.models import RentingSurveyModel
from cocoon.scheduler.models import ItineraryModel
from cocoon.scheduler.clientScheduler.client_scheduler import ClientScheduler
from cocoon.commutes.constants import CommuteAccuracy

# Python Modules
import json
from django.utils import dateparse
import datetime
import dateutil

# Rest Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response


@method_decorator(user_passes_test(lambda u: u.is_hunter or u.is_admin), name='dispatch')
class ItineraryFileView(TemplateView):
    """
    Loads the template for an individual itinerary
    """
    template_name = 'scheduler/itineraryFile.html'

    def dispatch(self, request, *args, **kwargs):
        itinerary_slug = kwargs.get('itinerary_slug')
        self.itinerary = get_object_or_404(ItineraryModel, url=itinerary_slug)
        self.tour_ordered_visits = [visit for visit in self.itinerary.ordered_homes.order_by("visit_index")]
        return super(ItineraryFileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)

        m, _ = divmod(self.itinerary.tour_duration_seconds_rounded, 60)
        h, m = divmod(m, 60)
        friendly_duration = "{0}h {1}m".format(h, m)

        destinations = []
        if self.itinerary.survey:
            tenants = self.itinerary.survey.tenants
            for t in tenants.all():
                destinations.append(t.full_address)

        visit_times = [
            list(ViableTourTimeModel.objects.filter(home_visit=home_visit).order_by("visit_time").all()) for home_visit in self.tour_ordered_visits
        ]

        start_times = self.itinerary.start_times

        # Survey load url
        current_site = get_current_site(self.request)
        survey_load_url = "https://{0}/survey/rent/{1}/".format(current_site.domain, self.itinerary.survey.url)

        context.update({
            'client': self.itinerary.client,
            'survey': self.itinerary.survey,
            'destinations': destinations,
            'itinerary_claimed': False if self.itinerary.agent is None else True,
            'agent': self.itinerary.agent,
            'tour_duration': friendly_duration,
            'is_scheduled': False if self.itinerary.selected_start_time is None else True,
            'start_time': self.itinerary.selected_start_time,
            'home_visits': self.tour_ordered_visits,
            'is_finished': self.itinerary.finished,
            'visit_times': visit_times,
            "start_times": start_times,
            "survey_url": survey_load_url,
        })
        return context


@method_decorator(login_required, name='dispatch')
class ClientSchedulerView(TemplateView):
    """
    Loads the template for the ClientScheduler

    The template has the entry point for React and react handles
        the rest of the frontend
    """
    template_name = 'scheduler/clientScheduler.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = ClientSchedulerView.__name__
        return data


@method_decorator(login_required, name='dispatch')
class AgentSchedulerPortalView(TemplateView):
    """
    Loads the template for the AgentSchedulerPortal

    The template contains the entry point for React and react handles
    retrieving the necessary data
    """
    template_name = 'scheduler/agentSchedulerPortal.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = AgentSchedulerPortalView.__name__
        return data


@method_decorator(login_required, name='dispatch')
class AgentSchedulerMarketplaceView(TemplateView):
    """
        Loads the template for the AgentSchedulerMarketplace

        The template contains the entry point for React and react handles
        retrieving the necessary data
        """
    template_name = 'scheduler/agentSchedulerMarketplace.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # Tells React which component to load onto the page
        data['component'] = AgentSchedulerMarketplaceView.__name__
        return data


class ItineraryViewset(viewsets.ReadOnlyModelViewSet):
    """
    Used for retrieving a generic itinerary. Base on the account type the user
    can get access to more itinerary models
    """

    serializer_class = ItinerarySerializer

    def get_serializer_context(self):
        """
        Gets the context data for the serializer so that broker accounts get the information regarding
            the home
        """
        return {'user': self.request.user}

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        if user_profile.user.is_broker or user_profile.user.is_admin:
            return ItineraryModel.objects.all()
        else:
            return ItineraryModel.objects.filter(client=user_profile.user)


@method_decorator(user_passes_test(lambda u: u.is_hunter or u.is_broker or u.is_admin), name='dispatch')
class ItineraryClientViewSet(viewsets.ModelViewSet):
    """
    Used on the client scheduler page to retrieve the itineraries for the current user
    """

    serializer_class = ItinerarySerializer

    def get_serializer_context(self):
        """
        Gets the context data for the serializer so that broker accounts get the information regarding
            the home
        """
        return {'user': self.request.user}

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return ItineraryModel.objects.filter(client=user_profile.user).filter(finished=False)

    def create(self, request, *args, **kwargs):
        """
        Creates an itinerary for a client. The survey id associated with the itinerary is passed in
            and the homes on that surveys visit list is added to the itinerary
        :param request:
        :param args:
        :param kwargs:
                Expects:
                    survey_id: (int) -> The id of the survey associated with the itinerary
        :return:
            {
                'results': (boolean) -> True: The itinerary was successfully created
                                        False: The itinerary was not successfully created
                'message': (string) -> A message related to the response
            }
        """
        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey associated with the itinerary
        if 'survey_id' in self.request.data:
            survey_id = self.request.data['survey_id']
            survey = get_object_or_404(RentingSurveyModel, id=survey_id, user_profile=user_profile)
        else:
            raise Http404

        homes_list = []
        for home in survey.visit_list.all():
            homes_list.append(home)

        # Run client_scheduler algorithm
        client_scheduler_alg = ClientScheduler(CommuteAccuracy.EXACT)
        result = client_scheduler_alg.save_itinerary(homes_list, self.request.user, survey)
        if result:
            return Response({
                'result': True,
                'message': 'Itinerary created'
            })
        else:
            return Response({
                'result': False,
                'message': 'Failed to created itinerary'
            })

    def update(self, request, *args, **kwargs):

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the itinerary id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated itinerary with the request
        itinerary = get_object_or_404(ItineraryModel, pk=pk, client=user_profile.user)

        # Save all the available start times the client indicated
        if 'start_times' in self.request.data['type']:
            start_times = self.request.data['start_times']

            # Loop through all the start_times so they can all be added
            for start_time in start_times:
                if 'time_available_seconds' in start_time:
                    time_available_seconds = start_time['time_available_seconds']
                    dt = dateutil.parser.parse(start_time['date'])
                    dt = dt.replace(second=0, microsecond=0)
                    itinerary.start_times.create(time=dt, time_available_seconds=time_available_seconds)

            # Generate potential visit times so agents can coordinate with property managers
            client_scheduler_alg = ClientScheduler(CommuteAccuracy.EXACT)
            client_scheduler_alg.generate_tour_times(user=user_profile.user)

            # Automatically set the agent assigned to the itinerary if the agent has a referred agent
            # Send an email to the appropriate people
            if user_profile.referred_agent is not None:
                itinerary.agent = user_profile.referred_agent
                itinerary.save()
                send_new_itinerary_referred_email(itinerary.agent)
            else:
                # Send an email to all the agents to indicate that a new home is in the marketplace
                for agent in MyUser.objects.all().filter(is_broker=True):
                    send_new_itinerary_marketplace_email(agent)

        # Retrieve the object again to get the updated fields
        itinerary = get_object_or_404(ItineraryModel, pk=pk, client=user_profile.user)
        serializer = ItinerarySerializer(itinerary)
        return Response(serializer.data)


@method_decorator(user_passes_test(lambda u: u.is_broker or u.is_admin), name='dispatch')
class ItineraryAgentViewSet(viewsets.ModelViewSet):
    """
    Used to pull the itineraries associated with that the current user which should be an agent
    """

    serializer_class = ItinerarySerializer

    def get_serializer_context(self):
        """
        Gets the context data for the serializer so that broker accounts get the information regarding
            the home
        """
        return {'user': self.request.user}

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        itinerary_type = self.request.query_params.get('type', None)

        if itinerary_type == 'unscheduled':
            return ItineraryModel.objects.filter(agent=user_profile.user, selected_start_time=None)\
                .exclude(finished=True)
        elif itinerary_type == 'scheduled':
            return ItineraryModel.objects.filter(agent=user_profile.user).exclude(selected_start_time=None)\
                .exclude(finished=True)
        else:
            raise Http404

    def update(self, request, *args, **kwargs):

        result = False
        reason = ''

        # Retrieve the user profile
        user_profile = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the itinerary id
        pk = kwargs.pop('pk', None)

        # Retrieve the associated itinerary with the request
        itinerary = get_object_or_404(ItineraryModel, pk=pk)

        # Case if an agent is trying to schedule an itinerary they already claimed
        if 'schedule' in self.request.data.get('type', None):
            iso_start_time = self.request.data.get('iso_str', None)
            if iso_start_time is not None:
                proposed_time, created = TimeModel.objects.get_or_create(
                    time=dateparse.parse_datetime(iso_start_time),
                    itinerary=itinerary,
                    time_available_seconds=itinerary.tour_duration_seconds_rounded)
                start_time_valid = False

                # find an available start time that works
                qs = TimeModel.objects.filter(itinerary=itinerary)
                for time_object in qs:
                    if proposed_time.time + datetime.timedelta(seconds=itinerary.tour_duration_seconds_rounded) <= \
                                    time_object.time + datetime.timedelta(seconds=time_object.time_available_seconds):
                        start_time_valid = True
                        break

                if start_time_valid:
                    itinerary.select_start_time(proposed_time.time)
                    result = True
                else:
                    result = False
                    reason = 'Start time is not valid given user preferences'

        # Case if the agent is trying to claim an itinerary from the market
        elif 'claim' in self.request.data['type']:

            # If the itinerary is already claimed then the agent cannot claim it anymore
            if itinerary.agent is None:
                itinerary.associate_agent(user_profile.user)
                result = True
            else:
                result = False
                reason = 'Itinerary already claimed'
        elif 'finish' in self.request.data['type']:

            if itinerary.agent.id is user_profile.user.id:
                itinerary.finished = True
                itinerary.save()
                result = True
            else:
                result = False
                reason = 'Only the assigned agent is allowed to finish the itinerary'

        return Response({'result': result,
                         'reason': reason})

    # allows agents to retrieve specific client itineraries
    def retrieve(self, request, *args, **kwargs):
        # Retrieve the itinerary id
        pk = kwargs.pop('pk', None)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        queryset = ItineraryModel.objects.filter(agent=user_profile.user)
        client_itinerary = get_object_or_404(queryset, pk=pk)
        serializer = ItinerarySerializer(client_itinerary)
        return Response(serializer.data)


class ClientItineraryCalculateDuration(viewsets.ViewSet):
    """
    Used to calculate the itinerary approximate duration to inform the user before
        they decide to schedule a group of homes
    """

    @staticmethod
    def list(request, *args, **kwargs):
        return Response({'message': 'List not implemented'})

    def retrieve(self, request, *args, **kwargs):
        """
        Given the survey passed via the url, returns the total duration to do the commute
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_prof = get_object_or_404(UserProfile, user=self.request.user)

        # Retrieve the survey id
        pk = kwargs.pop('pk', None)

        survey = get_object_or_404(RentingSurveyModel, pk=pk, user_profile=user_prof)
        homes_list = []
        for home in survey.visit_list.all():
            homes_list.append(home)

        # Run client_scheduler algorithm
        client_scheduler_alg = ClientScheduler(accuracy=CommuteAccuracy.APPROXIMATE)
        result = client_scheduler_alg.calculate_duration(homes_list)[0]
        return Response({'duration': result})


@method_decorator(user_passes_test(lambda u: u.is_broker or u.is_admin), name='dispatch')
class ItineraryMarketViewSet(viewsets.ModelViewSet):

    serializer_class = ItinerarySerializer

    def get_queryset(self):

        return ItineraryModel.objects.filter(agent=None).exclude(finished=True).exclude(start_times__isnull=True)


########################################
# AJAX Request Handlers
########################################

@login_required
def unschedule_itinerary(request):
    itinerary_id = request.POST.get('itinerary_id')
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_hunter:
        try:
            itinerary = ItineraryModel.objects.get(id=itinerary_id)
            if itinerary.client.id != current_profile.user.id:
                return HttpResponse(json.dumps({"result": "1"}),
                                    content_type="application/json")
            itinerary.unschedule_itinerary(request=request)
            return HttpResponse(json.dumps({"result": "0"}),
                                content_type="application/json",
                                )
        except ItineraryModel.DoesNotExist:
            return HttpResponse(json.dumps({"result": "1"}),
                                content_type="application/json",
                                )
    else:
        return HttpResponse(json.dumps({"result": "1"}),
                            content_type="application/json",
                            )

@login_required
def update_visit_time(request):
    visit_id = request.POST.get('id')
    visit_time = get_object_or_404(ViableTourTimeModel, id=visit_id)
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if current_profile.user.is_broker or current_profile.user.is_admin:
        try:
            availability = request.POST.get('availability')
            if availability in ['y', 'n', 'm']:
                visit_time.availability = availability
                visit_time.save()
                return HttpResponse(json.dumps({"result": "0"}),
                                    content_type="application/json",
                                    )
            else:
                return HttpResponse(json.dumps({"result": "1"}),
                             content_type="application/json",
                             )
        except KeyError:
            return HttpResponse(json.dumps({"result": "1"}),
                         content_type="application/json",
                         )
    return HttpResponse(json.dumps({"result": "1"}),
                            content_type="application/json",
                            )