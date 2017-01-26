from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Campaign, Partner


class CampaignShortSerializer(serializers.Serializer):
    content = serializers.CharField()


class CampaignSerializer(CampaignShortSerializer):
    partner_id = serializers.CharField()
    duration = serializers.DurationField()

    def create(self, validated_data):
        partner_id = validated_data.get('partner_id')
        p = Partner.objects.get(partner_id=partner_id)
        validated_data['partner_id'] = p.id
        return Campaign.objects.create(**validated_data)

    def validate(self, data):
        now = timezone.now()
        if any(Campaign.objects.select_related('partner').filter(
                partner__partner_id=data['partner_id'], finish_timestamp__gte=now)
        ):
            raise ValidationError('This Partner is already has active campaign')
        elif not Partner.objects.filter(partner_id=data['partner_id']).exists():
            raise ValidationError('There is no Partner with partner_id "%s"' % data['partner_id'])
        return data


class CampaignListSerializer(CampaignShortSerializer):
    partner = serializers.CharField()
    is_active = serializers.BooleanField()
