# Generated by Django 3.1 on 2021-02-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulelog',
            name='Comment',
            field=models.TextField(blank=True),
        ),
    ]