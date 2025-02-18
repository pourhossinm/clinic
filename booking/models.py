from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SERVICE_CHOICES = (
    ("Hearing", "شنوایی"),
    ("Speech therapy", "گفتار درمانی"),
    ("Occupational therapy", "کاردرمانی"),
    ("Physiotherapy", "فیزیوتراپی"),
    ("Arthritis", "آرتروز"),
    ("Prosthesis", "پروتز"),
    )
TIME_CHOICES = (
    ("8 صبح", "8:30 صبح"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
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

#     < h3
#
#     class ="" > انتخاب خدمات:<
#
#         / h3 >
#     < select
#
#     class ="form-select fs-3" name="service" >
#
#     < option
#     value = "Hearing" > شنوایی < / option >
#     < option
#     value = "Speech therapy" > گفتار
#     درمانی < / option >
#     < option
#     value = "Occupational therapy" > کاردرمانی < / option >
#     < option
#     value = "Physiotherapy" > فیزیوتراپی < / option >
#     < option
#     value = "Arthritis" > آرتروز < / option >
#     < option
#     value = "Prosthesis" > پروتز < / option >
#
# < / div >