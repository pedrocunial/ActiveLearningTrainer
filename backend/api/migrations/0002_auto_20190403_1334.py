# Generated by Django 2.2 on 2019-04-03 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentialobjectstorage',
            name='api_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='credentialobjectstorage',
            name='bucket_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='credentialobjectstorage',
            name='instance_id',
            field=models.CharField(max_length=255),
        ),
    ]
