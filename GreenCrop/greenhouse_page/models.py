from django.contrib.auth.models import User
from django.db import models


class Greenhouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imei = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    area = models.IntegerField(null=True, blank=True)
    sowing = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Greenhouse {self.id} - {self.location}"

class Alerts_gr(models.Model):
    ALERT_TYPES = [
        ('Температура', 'Температура'),
        ('Влажность', 'Влажность'),
        ('Вода', 'Вода'),
        ('Освещение', 'Освещение'),
        ('Оборудование', 'Оборудование'),
        ('Ошибка', 'Ошибка'),
    ]

    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    alerts_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.get_alerts_type_display()} - {self.greenhouse} - {self.datetime}"

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'

class Registry(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    water = models.IntegerField()
    temp1 = models.IntegerField()
    temp2 = models.IntegerField()
    temp3 = models.IntegerField()
    soil_moisture = models.IntegerField()
    air_humidity = models.IntegerField()
    energy_usage = models.IntegerField(null = True, blank=True)

    def __str__(self):
        return f"Registry {self.id} - {self.greenhouse.location} at {self.datetime}"


class GreenhouseControl(models.Model):
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    ventilation = models.BooleanField()
    window1 = models.BooleanField()
    window2 = models.BooleanField()
    water_supply = models.BooleanField()
    lights = models.BooleanField()

    def __str__(self):
        return f"Control {self.id} - {self.greenhouse.location}"


class Report(models.Model):
    REPORT_TYPES = [
        ('Состояние растений', 'Состояние растений'),
        ('Урожайность', 'Урожайность'),
        ('Погодные условия', 'Погодные условия'),
        ('Использование ресурсов', 'Использование ресурсов'),
        ('Состояние оборудования', 'Состояние оборудования'),
        ('Экономическая эффективность', 'Экономическая эффективность'),
        ('Анализ почвы', 'Анализ почвы'),
        ('Климатические условия', 'Климатические условия'),
    ]
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    type_report = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    rate_plants = models.IntegerField()

    def __str__(self):
        return f"Report {self.id} - {self.type_report} at {self.datetime}"
