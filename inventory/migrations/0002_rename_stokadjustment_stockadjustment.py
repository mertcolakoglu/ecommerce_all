# Generated by Django 5.1 on 2024-08-13 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StokAdjustment',
            new_name='StockAdjustment',
        ),
    ]
