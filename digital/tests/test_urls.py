from django.urls import reverse, resolve
from django.test import Client
from django.contrib.auth.models import User
from dsrs import models
import pytest

@pytest.mark.django_db
class TestUrls:

    def test_resources_percentile_url(self):
        path = reverse('resource-percentile', kwargs={'number': 10})
        assert resolve(path).view_name == 'resource-percentile'

        client = Client()
        payload = {
            'territory': 'SP',
            'period_start': '2020-01-01',
            'period_end': '2020-05-31'
        }
        response = client.get(path, payload)
        assert response.status_code == 200

    def test_admin_action_delete_dsr_resource_url(self):
        client = Client()
        user = User.objects.create_superuser(
            username='test',
            password='test',
        )
        client.force_login(user)
        mock_qs = models.DSR.objects.none()
        path = reverse('admin:dsrs_dsr_changelist', current_app='dsrs')
        response = client.post(path, {'action': 'delete_dsr_resource',
                                                '_selected_action': mock_qs
                                                    })
        assert response.status_code == 200
