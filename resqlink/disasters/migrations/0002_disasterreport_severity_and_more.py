# Generated by Django 5.1.7 on 2025-03-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disasters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='disasterreport',
            name='severity',
            field=models.CharField(choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High'), ('Critical', 'Critical')], default='Moderate', max_length=10),
        ),
        migrations.AlterField(
            model_name='disasterreport',
            name='disaster_type',
            field=models.CharField(choices=[('Flood', 'Flood'), ('Earthquake', 'Earthquake'), ('Fire', 'Fire'), ('Tornado', 'Tornado'), ('Hurricane', 'Hurricane'), ('Landslide', 'Landslide'), ('Tsunami', 'Tsunami'), ('Drought', 'Drought'), ('Volcanic Eruption', 'Volcanic Eruption'), ('Extreme Heat', 'Extreme Heat'), ('Snowstorm', 'Snowstorm'), ('Thunderstorm', 'Thunderstorm')], max_length=30),
        ),
        migrations.AlterField(
            model_name='disasterreport',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='disasterreport',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
