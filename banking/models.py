from django.db import models
from django.contrib.auth import get_user_model
import uuid



def generate_code():
    t = uuid.uuid4().hex
    return t


class AuthCode( models.Model):
    transfer_type = models.CharField(max_length= 10, choices = (
        ("local", "local"),
        ("intl", "intl")
    ), blank=False)
    transfer_id = models.UUIDField(blank = False, unique=True, max_length = 48)
    code = models.CharField(default= generate_code, unique=True, max_length = 48, editable = False)

    def __str__(self):
        return self.code


# model for local transfer request
class LocalTransferRequest(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="transfer_requests", on_delete=models.CASCADE)
    account_number = models.CharField(max_length=35, blank=False, )
    amount = models.PositiveIntegerField(blank=False)
    status = models.CharField(max_length=25, default= "Pending", choices=(
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
        ("Successful", "Successful"),
    ))
    
    tx_ref = models.UUIDField(default=uuid.uuid4, unique=True)
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "Local Transfers"
        verbose_name = "Local Transfer "

    @property
    def type(self):
        return "Local"

    @property
    def state(self):
        if self.verified:
            return "verified"
        return "Pending Verification"

    def __str__(self):
        return self.user.get_full_name() + " transfer request " + str(self.id)

# model for intl transfer request


class IntlTransferRequest(models.Model):
    user = models.ForeignKey(get_user_model(
    ), related_name="intl_transfer_requests", on_delete=models.CASCADE)
    account_number = models.CharField(max_length=35, blank=False)
    account_name = models.CharField(max_length=64)
    amount = models.PositiveIntegerField(blank=False)
    country = models.CharField(max_length=48, blank=False)
    swift_code = models.CharField(max_length=32)
    iban_code = models.CharField(max_length=32)
    bank_address = models.CharField(max_length=128)
    bank_name = models.CharField(max_length=128)
    verified = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(blank=False)
    status = models.CharField(max_length=35, default= "Pending",  choices=(
        ("Successful", "Successful"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled")
    ))
    
    tx_ref = models.UUIDField(default=uuid.uuid4, unique=True)
    date = models.DateTimeField(auto_now_add=True )

    class Meta:
        verbose_name = "International Transfer"
        verbose_name_plural = "International Transfers"

    def __str__(self):
        return self.user.get_full_name() + "   intl transfer request " + str(self.id)
    
    @property
    def type(self):
        return "International"


    @property
    def state(self):
        if self.verified:
            return "Verified"
        return "Pending Verification"

# model for withdrawals


class WithdrawalHistory(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="history_set", on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=(
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
        ("Successful", "Successful"),
    ))
    tx_ref = models.UUIDField(default=uuid.uuid4, unique=True)
    date = models.DateTimeField(auto_now_add=True )
    amount = models.PositiveIntegerField(blank=False)

    class Meta:
        verbose_name_plural = "Histories"

    def __str__(self):
        return "History " + str(self.id)


# UserAccount


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        get_user_model(), related_name="account", on_delete=models.CASCADE)

    account_type = models.CharField(max_length=30, choices=(
        ("Tier 1", "Tier 1"),
        ("Tier 2", "Tier 2")
    ), default="Tier 1")

    balance = models.PositiveIntegerField(default=0)

    last_modified = models.DateTimeField(auto_now=True)

    date_created = models.DateTimeField(auto_now_add=True)

    account_number = models.CharField(
        max_length=48, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return self.account_number
