import time

from datetime import timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from .models import Partner, Campaign


class CampaignApiTestCase(APITestCase):

    def setUp(self):

        user = User.objects.create(
            username='test_user',
            password=User.objects.make_random_password(),
            email='test_user@example.com'
        )
        self.partner = Partner.objects.create(partner_id='abc', user=user)
        self.create_url = reverse('campaign_create')
        self.detail_url = reverse('campaign_detail', args=[self.partner.partner_id])
        self.list_url = reverse('campaign_list')

    def test_get_create(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 405)

    def test_post_create(self):
        data = {
            'content': 'test content',
            'partner_id': self.partner.partner_id,
            'duration': 3
        }
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

        # next request should fail, because there is an active campaign
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)

        print('Waiting 3 sec for campaign expired')
        time.sleep(3)

        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_detail(self):
        campaigns = Campaign.objects.all()
        campaigns.delete()
        duration = timedelta(seconds=20)
        Campaign.objects.create(partner=self.partner, duration=duration, content='content')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
