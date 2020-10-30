from django.contrib import admin

# Register your models here.
from .models import Medicines, medicine_type
admin.site.register(Medicines)
admin.site.register(medicine_type)