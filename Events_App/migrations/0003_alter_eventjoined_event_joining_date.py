# Generated by Django 3.2.8 on 2021-10-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events_App', '0002_eventjoined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventjoined',
            name='event_joining_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]