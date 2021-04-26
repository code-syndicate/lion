# Generated by Django 3.1.6 on 2021-04-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0007_auto_20210328_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='intltransferrequest',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='debit', max_length=25, verbose_name='Transaction type'),
        ),
        migrations.AddField(
            model_name='localtransferrequest',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='debit', max_length=25, verbose_name='Transaction type'),
        ),
    ]
