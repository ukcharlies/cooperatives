# Generated by Django 5.0.6 on 2024-07-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
