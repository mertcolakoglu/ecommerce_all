# Generated by Django 5.1 on 2024-08-07 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name_surname', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=13)),
                ('address', models.TextField(blank=True)),
                ('is_supplier', models.BooleanField(default=False)),
            ],
        ),
    ]