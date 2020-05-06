from django.contrib import admin

# Register your models here.
from .models import Coach, Athlete, Box, Exercise

admin.site.register(Box)
admin.site.register(Exercise)
admin.site.register(Coach)
admin.site.register(Athlete)