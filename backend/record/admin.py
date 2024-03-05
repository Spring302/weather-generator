from django.contrib import admin
from .models import LoginAccess, DailyRecord

# Register your models here.
admin.site.register(LoginAccess)
admin.site.register(DailyRecord)
