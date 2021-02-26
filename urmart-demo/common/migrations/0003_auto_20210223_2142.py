# Generated by Django 3.1 on 2021-02-23 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_remove_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='CreatedTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='LastModified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='CreatedTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='LastModified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
