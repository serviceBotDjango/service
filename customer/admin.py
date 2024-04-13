from django.contrib import admin

from .models import Customer, Log, DeviceType, Manufacturer, Application, Refilling, Review

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Customer)
admin.site.register(Log)
admin.site.register(DeviceType)
admin.site.register(Manufacturer)
admin.site.register(Application)
admin.site.register(Refilling)
admin.site.register(Review)



