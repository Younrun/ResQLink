# Generated by Django 5.1.7 on 2025-03-13 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disasters', '0002_disasterreport_severity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disasterreport',
            name='latitude',
            field=models.DecimalField(decimal_places=8, max_digits=11),
        ),
        migrations.AlterField(
            model_name='disasterreport',
            name='longitude',
            field=models.DecimalField(decimal_places=8, max_digits=11),
        ),
    ]
