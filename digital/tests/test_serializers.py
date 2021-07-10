from mixer.backend.django import mixer
import pytest
from dsrs import serializers
from dsrs import models

'''
With proper use of mixture and ORM, test can be improved.
'''

@pytest.mark.django_db
class TestSerializers:

    def test_DSRSerializers_create(self):
        request_data = {
                            "path": "my_data/Spotify_SpotifyDuo_SGAE_NO_NOK_20200101-20200531.tsv",
                            "period_start": "2020-01-01",
                            "period_end": "2020-05-31",
                            "status": "ingested",
                            "territory": {
                                "name": "SPAIN",
                                "code_2": "SP"
                            },
                            "currency": {
                                "name": "EURO",
                                "code": "EUR"
                            }
                        }

        result = serializers.DSRSerializer().create(request_data)
        assert result['status'] == True

    def test_ResourceSerializers_create(self):
        request_data = {
                "dsp_id": "gdkXSptopEXhLvWLXfwQUqiqEXYOTE",
                "title": "accept media",
                "artists": "Breanna Moran|Rebecca Dickerson",
                "isrc": "EROVR1717158",
                "usages": "790077",
                "revenue": "65.0",
                "dsrs_id": 2
            }

        result = serializers.ResourceSerializer(data=request_data)
        assert result.is_valid() == True
