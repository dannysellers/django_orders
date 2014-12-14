from django.contrib import admin
import models

admin.site.register(models.Customer)
admin.site.register(models.Inventory)
admin.site.register(models.Operation)