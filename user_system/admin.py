from django.contrib import admin

# Register your models here.

from .models import UserPersonalized

admin.site.register(UserPersonalized)