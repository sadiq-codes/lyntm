from rest_framework import serializers


class PinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4)
