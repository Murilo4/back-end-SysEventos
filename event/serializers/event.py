from rest_framework import serializers
from ..models import Event


class CreateEvent(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'data', 'horario_inicio', 'horario_final',
                  'descricao', 'photo', 'event_creator']

    def create(self, validated_data):
        event = Event(**validated_data)
        event.save()
        return event


class CreateQrCode(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['qr_code']

    def create(self, validated_data):
        event = Event(**validated_data)
        event.save()
        return event


class UpdateEvent(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['data', 'horario_inicio', 'horario_final',
                  'descricao', 'photo']

    def update(self, instance, validated_data):
        instance.data = validated_data.get(
            'data', instance.data)
        instance.horario_inicio = validated_data.get(
            'horario_inicio', instance.horario_inicio)
        instance.horario_final = validated_data.get(
            'horario_final', instance.horario_final)
        instance.descricao = validated_data.get(
            'descricao', instance.descricao)
        instance.photo = validated_data.get(
            'photo', instance.photo)

        instance.save()

        return instance


class StartEvent(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['is_active']

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()

        return instance
