# Generated by Django 3.1.6 on 2021-03-28 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intltransferrequest',
            options={'verbose_name': 'International Transfer', 'verbose_name_plural': 'International Transfers'},
        ),
        migrations.AlterModelOptions(
            name='localtransferrequest',
            options={'verbose_name': 'Local Transfer ', 'verbose_name_plural': 'Local Transfers'},
        ),
    ]