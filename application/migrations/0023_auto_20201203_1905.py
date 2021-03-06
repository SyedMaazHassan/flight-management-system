# Generated by Django 3.0.3 on 2020-12-03 14:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0022_auto_20201201_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountcredits',
            options={'verbose_name_plural': 'AccountCredit'},
        ),
        migrations.AlterField(
            model_name='airline',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 19, 5, 46, 585067), editable=False),
        ),
        migrations.AlterField(
            model_name='airplane',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 3, 19, 5, 46, 585067), editable=False),
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
