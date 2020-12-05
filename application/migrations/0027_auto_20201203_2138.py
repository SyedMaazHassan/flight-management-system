# Generated by Django 3.0.3 on 2020-12-03 16:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0026_auto_20201203_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseticket',
            name='ticket_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='airline',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 21, 38, 10, 808763), editable=False),
        ),
        migrations.AlterField(
            model_name='airplane',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 21, 38, 10, 809762), editable=False),
        ),
    ]
