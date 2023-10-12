from rest_framework import serializers
from .models import Bootcamp_client

class BootcampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bootcamp_client
        fields = '__all__'