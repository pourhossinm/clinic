from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SERVICE_CHOICES = (
    ("شنوایی", "شنوایی"),
    ("Speech therapy", "Speech therapy"),
    ("Occupational therapy", "Occupational therapy"),
    ("Physiotherapy", "Physiotherapy"),
    ("Arthritis", "آArthritis"),
    ("Prosthesis", "Prosthesis"),
    )
TIME_CHOICES = (
    ("8 AM", "8:30 AM"),
    ("8:30 AM", "9 AM"),
    ("9 AM", "9:30 AM"),
    ("9:30 AM", "10 AM"),
    ("10: AM", "10:30 AM"),
    ("10:30 AM", "11 AM"),
    ("11 AM", "11:30 AM"),
    ("11:30 AM", "12 AM"),
    ("3 PM", "3:30 9M"),
    ("3:30 PM", "4 PM"),
    ("4 PM", "4:30 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Doctor care")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"

