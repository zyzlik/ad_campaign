from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Partner(models.Model):
    partner_id = models.SlugField(verbose_name='Unique ID for partner', unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        app_label = 'ad_campaign'

    def __str__(self):
        return '%s: %s' % (self.partner_id, self.user.username)


class Campaign(models.Model):
    partner = models.ForeignKey(Partner)
    duration = models.DurationField(verbose_name='Campaign duration in seconds')
    content = models.TextField(verbose_name='Campaign content')
    create_timestamp = models.DateTimeField(auto_now_add=True)
    finish_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'ad_campaign'

    def __str__(self):
        return self.content

    @property
    def is_active(self):
        now = timezone.now()
        return self.finish_timestamp > now

    def clean(self, *args, **kwargs):
        now = timezone.now()
        if any(Campaign.objects.filter(partner=self.partner, finish_timestamp__gte=now)):
            raise ValidationError('This Partner is already has active campaign')

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.finish_timestamp:
            self.finish_timestamp = now + self.duration
        super(Campaign, self).save(*args, **kwargs)
