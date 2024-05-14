from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
# Create your models here.


class AccessKey(models.Model):
    "Access Key Model"
    STATUS_CHOICES = [('active', 'Active'), ('expired', 'Expired'), ('revoked', 'Revoked')]
    name = models.CharField(max_length=100,unique=True,blank=False,null=False)
    key = models.CharField(max_length=100,unique=True,default=uuid4())
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='active')
    procurement_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=20))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ['-procurement_date']


    def set_status(self,status):
        "Sets the status of the access key"
        previous_status = self.status
        if previous_status != status and previous_status == "active":
            self.status = status
            self.save()
            
