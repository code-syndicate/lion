# Generated by Django 3.1.6 on 2021-03-28 19:06

import banking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0006_auto_20210328_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='intltransferrequest',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='localtransferrequest',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='authcode',
            name='code',
            field=models.CharField(default=banking.models.generate_code, editable=False, max_length=48, unique=True),
        ),
    ]
