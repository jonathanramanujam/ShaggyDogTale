from django.contrib import admin
from .models import Story, Contribution,Vote

# Register your models here.
admin.site.register(Story)
admin.site.register(Contribution)
admin.site.register(Vote)
