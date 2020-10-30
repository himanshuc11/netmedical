from django.contrib.auth.models import AbstractUser
from django.db import models

class medicine_type(models.Model):
    medicine_genre = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.medicine_genre}"

class Medicines(models.Model):
    name = models.CharField(max_length=1000)
    manufaturer = models.CharField(max_length=1000)
    price = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    key_benifits = models.CharField(max_length=1000)
    dosage = models.CharField(max_length=1000)
    safety_info = models.CharField(max_length=1000)
    other_info = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/')
    genres = models.ManyToManyField(medicine_type, blank=True, null=True, related_name="Medicines")

    def __str__(self):
        return f"{self.name}"
