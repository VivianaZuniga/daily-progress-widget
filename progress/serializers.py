from rest_framework import serializers
from .models import Activity, DailyLog

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class DailyLogSerializer(serializers.ModelSerializer):
    activity_name = serializers.ReadOnlyField(source='activity.name')

    class Meta:
        model = DailyLog
        fields = ['id', 'date', 'activity', 'activity_name', 'complete']