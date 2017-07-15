# string related field -> serializer relations
from .models import *
from rest_framework import serializers


class SatelliteSerializer(serializers.ModelSerializer):
    agency = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Satellite
        fields = ('id', 'name', 'longi', 'lati', 'alti', 'date', 'agency')


class SatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SatHistory
        fields = '__all__'


