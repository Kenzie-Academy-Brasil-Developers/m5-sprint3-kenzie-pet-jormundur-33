from rest_framework import serializers
from .models import Characteristic


class CharacteristicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        instance, _ = Characteristic.objects.get_or_create(**validated_data)
        return instance