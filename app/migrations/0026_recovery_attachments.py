# Generated by Django 3.1.12 on 2021-11-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20211028_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='recovery',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='Recovery Attachments'),
        ),
    ]