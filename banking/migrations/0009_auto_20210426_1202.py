# Generated by Django 3.1.6 on 2021-04-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0008_auto_20210426_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='intltransferrequest',
            name='date_initiated',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Initiated'),
        ),
        migrations.AddField(
            model_name='localtransferrequest',
            name='date_initiated',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Initiated'),
        ),
    ]
