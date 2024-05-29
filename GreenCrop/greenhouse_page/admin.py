from django.contrib import admin
from greenhouse_page.models import *

class GreenhousesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'imei', 'location', 'latitude', 'longitude', 'area', 'sowing')
    search_fields = ('user__username', 'imei', 'location')

class RegistryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'greenhouse', 'datetime', 'water', 'temp1', 'temp2', 'temp3', 'soil_moisture', 'air_humidity', 'energy_usage')
    search_fields = ('greenhouse__imei',)
    list_filter = ('datetime',)

class GreenhouseControlAdmin(admin.ModelAdmin):
    list_display = ('pk', 'greenhouse', 'ventilation', 'window1', 'window2', 'water_supply', 'lights')
    search_fields = ('greenhouse__imei',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'greenhouse', 'datetime', 'type_report', 'description', 'rate_plants')
    search_fields = ('greenhouse__imei', 'type_report')
    list_filter = ('datetime', 'type_report')

class AlertsGrAdmin(admin.ModelAdmin):
    list_display = ('pk', 'greenhouse', 'alerts_type', 'datetime', 'message')
    list_filter = ('alerts_type', 'datetime')
    search_fields = ('message', 'greenhouse__imei')
    ordering = ('-datetime',)

admin.site.register(Alerts_gr, AlertsGrAdmin)
admin.site.register(Greenhouse, GreenhousesAdmin)
admin.site.register(Registry, RegistryAdmin)
admin.site.register(GreenhouseControl, GreenhouseControlAdmin)
admin.site.register(Report, ReportAdmin)
