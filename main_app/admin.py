from django.contrib import admin
from main_app.models import Finch
from .models import Finch, Feeding

# Register your models here.
admin.site.register(Finch)
admin.site.register(Feeding)