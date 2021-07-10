from rest_framework import serializers
from django.core.serializers import serialize
import json

from . import models


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Territory
        fields = (
            "name",
            "code_2",
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = (
            "name",
            "code",
        )


class DSRSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = models.DSR
        fields = (
            "id",
            "path",
            "period_start",
            "period_end",
            "status",
            "territory",
            "currency",
        )

    def create(self, request_data):
        '''
        duplicate currecny & territory problem. will be fixed in v2
        '''
        try:
            '''
            if we use web interface
            {'csrfmiddlewaretoken': 'IyEUUKnw7hEpCwn7357PZXVrL7hgCMJdnsjdyplZ8y3KJHDU4H73NxAacSDJF6nD',
             'currency.code': '33',
             'currency.name': 'ww',
             'path': 'dsffasd',
             'period_end': '2021-03-23',
             'period_start': '2021-03-16',
             'status': 'ingested',
             'territory.code_2': '22',
             'territory.name': 'ad'}
            if we use postman, we need to send the data as
            {
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
            '''
            try:
                territory_data = {
                            'name': request_data['territory.name'],
                            'code_2': request_data['territory.code_2'],
                            }
                currency_data = {
                    'name': request_data['currency.name'],
                    'code': request_data['currency.code'],
                    }
                dsr_data = {
                    'path': request_data['path'],
                    'period_end': request_data['period_end'],
                    'period_start': request_data['period_start'],
                    'status': request_data['status'],
                    }
            except:
                territory_data = request_data.pop('territory')
                currency_data = request_data.pop('currency')
                dsr_data = request_data
                
            # duplicacy problem, get_or_create can be used.
            currency_obj = models.Currency.objects.create(**currency_data)
            territory_obj = models.Territory.objects.create(local_currency=currency_obj, **territory_data)
            dsr_obj = models.DSR.objects.create(
                currency=currency_obj,
                territory=territory_obj,
                **dsr_data
                )
            dsr_obj.save()
        except Exception as e:
            return {'status': False, 'msg': str(e)}



        return {'status': True, 'msg': ''}

class ResourceSerializer(serializers.ModelSerializer):
    # need dsr
    class Meta:
        model = models.Resource
        fields = (
            "id",
            "dsp_id",
            "title",
            "artists",
            "isrc",
            "usages",
            "revenue",
            "dsrs_id"
        )

    # not a good place to write business logic, will fix in v2
    @staticmethod
    def calculate_percentile(number, get_data):
        '''
        https://www.dummies.com/education/math/statistics/how-to-calculate-percentiles-in-statistics/
        implemented this theory. this query may be optimized
        This answer seems good but I do not understand fully
        https://stackoverflow.com/questions/41420998/calculating-percentile-from-django-queryset
        '''
        # validaiton of input
        try:
            percent = int(number)
            if number > 100 or number < 1:
                raise ValueError
        except Exception as e:
            print(e)
            return [422, False]

        where_clause = []
        if get_data.get('territory', False):
            where_clause.append('territory.code_2' + '="' + get_data['territory'].strip() + '"')

        if get_data.get('period_start', False):
            where_clause.append('dsr.period_start' + '>="' + get_data['period_start'].strip() + '"')
        if get_data.get('period_end', False):
            where_clause.append('dsr.period_end' + '<="' + get_data['period_end'].strip() + '"')


        # confused about ORM, did it manually
        sql = '''
            SELECT resource.id, resource.dsp_id, resource.title, resource.artists,
            resource.isrc, resource.usages, resource.revenue, resource.dsrs_id,
            dsr.currency_id, dsr.territory_id, territory.name, territory.code_2,
            currency.name, currency.code
            FROM resource
            INNER JOIN dsr ON resource.dsrs_id = dsr.id
            INNER JOIN currency ON currency.id = dsr.currency_id
            INNER JOIN territory ON territory.id = dsr.territory_id
            WHERE <where clause>
            ORDER BY resource.revenue ASC;
        '''
        if len(where_clause) > 0:
            sql = sql.replace('<where clause>', ' AND '.join(where_clause))
        else:
            sql = sql.replace('WHERE <where clause>', '')


        try:
            queryset = models.Resource.objects.raw(sql)
            total_count = len(queryset)
            index = round((percent/100) * total_count)

            top_percentile = queryset[index:]

            return [[x['fields'] for x in json.loads(serialize('json', top_percentile))], True]

        except Exception as e:
            print(e)
            return [503, False]
