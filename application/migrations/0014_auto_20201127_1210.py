# Generated by Django 3.1.2 on 2020-11-27 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auto_20201127_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airline',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 12, 10, 10, 947573), editable=False),
        ),
        migrations.AlterField(
            model_name='airplane',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 12, 10, 10, 947573), editable=False),
        ),
    ]
