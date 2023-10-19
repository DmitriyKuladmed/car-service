# Generated by Django 4.2.3 on 2023-07-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice_app', '0002_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='sum_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='in_basket',
            field=models.BooleanField(default=False),
        ),
    ]
