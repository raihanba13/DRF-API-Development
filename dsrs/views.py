from rest_framework import viewsets
from rest_framework.decorators import action
import csv
from rest_framework import status
from rest_framework.response import Response

from . import models, serializers



class DSRViewSet(viewsets.ModelViewSet):
    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer

    def create(self, request):
        # we may do this task with one create method
        dsr_serilizer = serializers.DSRSerializer(data=request.data)
        if dsr_serilizer.is_valid():
            result = serializers.DSRSerializer.create(dsr_serilizer, request.data)
            if result['status']:
                return Response({'msg': 'Operation successful.'}, status=status.HTTP_201_CREATED)
            else:
                # we can log the result['msg'] for debugging purpose
                print(result['msg'])
                return Response({'msg': 'Server down. Please try later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(dsr_serilizer.errors)
            return Response({'msg': 'Operation failed. Please check input data'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer

    @action(detail=False, methods=['post'])
    def add_resource_from_csv(self, request):
        try:
            csv_reader = csv.DictReader(request.FILES['file'].read().decode('utf-8').splitlines(), delimiter='\t')
            dsrs_data = int(request.data.get('dsrs_id'))
            
            # using ORM right way can do this also
            dsrs_data_check = models.DSR.objects.filter(id=dsrs_data)
            if len(dsrs_data_check) == 0:
                raise ValueError
        except:
            return Response({'msg': 'Operation failed. Please check input data'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        for row in csv_reader:
            row['dsrs_id'] = dsrs_data
            '''
            I am forcing these fields to pass validaiton. Pandas is a better option for data cleaning.
            we can log the invalid rows and take measurement about that
            '''
            try:
                row['usages'] = float(row['usages'])
            except:
                row['usages'] = 0

            try:
                row['revenue'] = float(row['revenue'])
            except:
                row['revenue'] = 0

            resource_serializer = serializers.ResourceSerializer(data=row)
            if resource_serializer.is_valid():
                resource_serializer.save()
            else:
                pass
                # we can log this data  
                # print(row)
                # print(resource_serializer.errors)
                # print('===================')

        return Response({'msg': 'Operation successful.'}, status=status.HTTP_201_CREATED)
   
    @action(detail=False, name='resource-percentile')
    def resources_percentile(self, request, number):
        result = serializers.ResourceSerializer.calculate_percentile(number, request.GET)

        if result[1]:
            return Response({'msg': 'Operation successful.','data': str(result[0])}, status=status.HTTP_200_OK)
        elif not result[1] and result[0] == 422:
            return Response({'msg': 'Operation failed. Please check input data'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif not result[1] and result[0] == 503:
            return Response({'msg': 'Service unavailable. Please try later.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
