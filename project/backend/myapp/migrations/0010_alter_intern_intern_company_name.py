# Generated by Django 3.2.25 on 2024-05-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20240526_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intern',
            name='intern_company_name',
            field=models.CharField(max_length=255),
        ),
    ]
