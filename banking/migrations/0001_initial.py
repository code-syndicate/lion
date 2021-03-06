# Generated by Django 3.1.6 on 2021-03-27 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Successful', 'Successful')], max_length=25)),
                ('tx_ref', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Histories',
            },
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Tier 1', 'Tier 1'), ('Tier 2', 'Tier 2')], default='Tier 1', max_length=30)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account_number', models.CharField(max_length=48, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bank Account',
                'verbose_name_plural': 'Bank Accounts',
            },
        ),
        migrations.CreateModel(
            name='LocalTransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=35)),
                ('amount', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Successful', 'Successful')], default='Pending', max_length=25)),
                ('tx_ref', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Local Transfer Request',
                'verbose_name_plural': 'Local Transfer Requests',
            },
        ),
        migrations.CreateModel(
            name='IntlTransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=35)),
                ('account_name', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=48)),
                ('swift_code', models.CharField(max_length=32)),
                ('iban_code', models.CharField(max_length=32)),
                ('bank_address', models.CharField(max_length=128)),
                ('bank_name', models.CharField(max_length=128)),
                ('amount', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('Successful', 'Successful'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=35)),
                ('tx_ref', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intl_transfer_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'International Transfer Request',
                'verbose_name_plural': 'International Transfer Requests',
            },
        ),
    ]
