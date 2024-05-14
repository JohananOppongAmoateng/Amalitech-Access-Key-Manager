from django.core.management.base import BaseCommand
from datetime import datetime
from  accesskey.models import AccessKey


class Command(BaseCommand):
    help = "Update the expired keys status"

    def handle(self, *args, **kwags):
        active_keys = AccessKey.objects.filter(status='active',expiry_date__lte=datetime.now())
        for key in active_keys:
            key.status = 'expired'
            key.save()