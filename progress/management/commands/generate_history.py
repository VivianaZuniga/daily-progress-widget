from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from progress.models import Activity, DailyLog

class Command(BaseCommand):
    help = 'Generates random history of the last 25 days for testing purposes.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        activities = Activity.objects.all()

        if not activities.exists():
            self.stdout.write(self.style.WARNING("First add activities to your widget before running this."))
            return

        self.stdout.write(f"Generating a fake history for {activities.count()} activities...")

        for i in range(1, 26):
            last_date = today - timedelta(days=i)

            for activity in activities:
                register, create = DailyLog.objects.get_or_create(
                    date=last_date,
                    activity=activity
                )
                register.complete = random.choice([True, False])
                register.save()

        self.stdout.write(self.style.SUCCESS("History generated successfully! You can now open the widget."))