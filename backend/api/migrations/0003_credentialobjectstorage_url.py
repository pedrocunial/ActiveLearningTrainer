# Generated by Django 2.2 on 2019-04-04 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190403_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentialobjectstorage',
            name='url',
            field=models.CharField(default='s3.us-south.cloud-object-storage.appdomain.cloud', max_length=255),
            preserve_default=False,
        ),
    ]