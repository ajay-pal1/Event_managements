from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    event_name=models.CharField(max_length=300)
    seats_available=models.IntegerField()
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    joining_start_date=models.DateTimeField()
    joining_end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.event_name

class EventJoined(models.Model):
    user_profile = models.ForeignKey(User,on_delete=models.CASCADE)
    event_name=models.ForeignKey(Event,on_delete=models.CASCADE)
    event_joining_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_profile.username