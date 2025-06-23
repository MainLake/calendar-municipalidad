# calendar_main/serializers.py (Example)
from rest_framework import serializers
from calendar_main.models import Event, EventType, Department, Contact, AdditionalObservation

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AdditionalObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalObservation
        fields = '__all__'