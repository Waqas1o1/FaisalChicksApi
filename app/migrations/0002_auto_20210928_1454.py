# Generated by Django 3.0 on 2021-09-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='default_price',
        ),
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='pakage_weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='sales_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Pellet', 'Pellet'), ('CRUMSS', 'CRUMSS')], default=1, max_length=300),
            preserve_default=False,
        ),
    ]
