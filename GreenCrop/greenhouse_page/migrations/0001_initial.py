# Generated by Django 5.0.6 on 2024-05-25 20:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Greenhouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GreenhouseControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ventilation', models.BooleanField()),
                ('window1', models.BooleanField()),
                ('window2', models.BooleanField()),
                ('water_supply', models.BooleanField()),
                ('lights', models.BooleanField()),
                ('greenhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhouse_page.greenhouse')),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('water', models.IntegerField()),
                ('temp1', models.IntegerField()),
                ('temp2', models.IntegerField()),
                ('temp3', models.IntegerField()),
                ('soil_moisture', models.IntegerField()),
                ('air_humidity', models.IntegerField()),
                ('greenhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhouse_page.greenhouse')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('type_report', models.CharField(choices=[('Состояние растений', 'Состояние растений'), ('Урожайность', 'Урожайность'), ('Погодные условия', 'Погодные условия'), ('Использование ресурсов', 'Использование ресурсов'), ('Состояние оборудования', 'Состояние оборудования'), ('Экономическая эффективность', 'Экономическая эффективность'), ('Анализ почвы', 'Анализ почвы'), ('Климатические условия', 'Климатические условия')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('rate_plants', models.CharField(max_length=10)),
                ('greenhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhouse_page.greenhouse')),
            ],
        ),
    ]