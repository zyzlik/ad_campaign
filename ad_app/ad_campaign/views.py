from django.http import Http404
from django.utils import timezone, six

from rest_framework import generics, status
from rest_framework.compat import set_rollback
from rest_framework.response import Response

from .serializers import CampaignSerializer, CampaignListSerializer, CampaignShortSerializer
from .models import Campaign


class CampaignCreate(generics.CreateAPIView):
    serializer_class = CampaignSerializer


class CampaignRetrieve(generics.RetrieveAPIView):
    serializer_class = CampaignShortSerializer
    lookup_field = 'partner__partner_id'
    lookup_url_kwarg = 'partner_id'

    def get_queryset(self):
        now = timezone.now()
        queryset = Campaign.objects.select_related('partner').filter(
            finish_timestamp__gt=now)
        return queryset

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            msg = 'There is no active campaign for that Partner'
            data = {'detail': six.text_type(msg)}

            set_rollback()
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            return super(CampaignRetrieve, self).handle_exception(exc)


class CampaignList(generics.ListAPIView):
    serializer_class = CampaignListSerializer
    queryset = Campaign.objects.select_related('partner').order_by('-finish_timestamp')
