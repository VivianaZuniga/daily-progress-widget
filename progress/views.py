from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Activity, DailyLog
from .serializers import ActivitySerializer, DailyLogSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class DailyLogViewSet(viewsets.ModelViewSet):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer

class ProgressAPIView(APIView):
    def get(self, request):
        today = timezone.now().date()

        activities = Activity.objects.all()
        for activity in activities:
            DailyLog.objects.get_or_create(date=today, activity=activity)

        register_today = DailyLog.objects.filter(date=today)

        total_today = register_today.count()
        complete_today = register_today.filter(complete=True).count()
        daily_percentage = (complete_today / total_today * 100) if total_today > 0 else 0

        selected_range = request.query_params.get('range', 'monthly')
        days = 30
        if selected_range == 'biannual':
            days = 180
        elif selected_range == 'annual':
            days = 365

        start_date = today - timedelta(days=days)
        records_period = DailyLog.objects.filter(date__range=[start_date, today])

        total_period = records_period.count()
        complete_period = records_period.filter(complete=True).count()
        percentage_period = (complete_period / total_period * 100) if total_period > 0 else 0

        return Response({
            "daily_percentage": {
                "percentage": round(daily_percentage, 2)
            },
            "daily_progress": {
                "tasks": DailyLogSerializer(register_today, many=True).data
            },
            "historical_percentage": {
                "requested_range": selected_range,
                "days_evaluated": days,
                "percentage": round(percentage_period, 2)
            }
        })

class HeatMapCalendarAPIView(APIView):
    def get(self, request):
        today = timezone.now().date()
        map_data = []

        for i in range(34, -1, -1):
            date_evaluate = today - timedelta(days=i)
            register = DailyLog.objects.filter(date=date_evaluate)

            total = register.count()
            completed = register.filter(complete=True).count()

            percentage = (completed / total * 100) if total > 0 else -1

            map_data.append({
                "date": date_evaluate.strftime("%Y-%m-%d"),
                "percentage": round(percentage, 2)
            })

        return Response(map_data)