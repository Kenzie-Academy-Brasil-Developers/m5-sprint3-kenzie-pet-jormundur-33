from rest_framework import serializers
from characteristics.models import Characteristic
from characteristics.serializers import CharacteristicSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from .models import Animal


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data):
        group_data = validated_data.pop("group")
        char_data = validated_data.pop("characteristics")
        group, _ = Group.objects.get_or_create(**group_data)
        chars = [
            Characteristic.objects.get_or_create(**c)[0] for c in char_data
        ]
        animal = Animal.objects.create(**validated_data, group=group)
        animal.characteristics.add(*chars)
        return animal

    def update(self, instance, validated_data):
        char_data = validated_data.pop("characteristics")
        chars = [
            Characteristic.objects.get_or_create(**c)[0] for c in char_data
        ]
        instance.characteristics.add(*chars)
        non_editable_keys = ("group", "sex")

        for key, value in validated_data.items():
            if key in non_editable_keys:
                raise KeyError
            setattr(instance, key, value)

        instance.save()
        return instance