import secrets
from django.db import models

from instructor.models import Instructor
from course.models import Course


class Wallet(models.Model):
    wallet_owner = models.ForeignKey(
        Instructor, null=True, on_delete=models.CASCADE, related_name="my_wallet")
    balance = models.FloatField(default=0.00)
    account_number = models.PositiveIntegerField(null=True, default=0)
    wallet_ref = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.wallet_owner.firstname} {self.wallet_owner.lastname}\'s wallet'

    def save(self, *args, **kwargs):
        while not self.wallet_ref:
            ref = secrets.token_urlsafe(16)
            is_wallet_ref = Wallet.objects.filter(wallet_ref=ref)
            if not is_wallet_ref.exists():
                self.wallet_ref = ref
        return super(Wallet, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "wallet"


class TransactionLog(models.Model):
    pass


class Payment(models.Model):
    course_to_enroll = models.ForeignKey(Course, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        while not self.reference:
            ref = secrets.token_urlsafe(50)
            object = Payment.objects.filter(reference=ref)
            if not object:
                self.reference = ref
        super(Payment, self).save(*args, **kwargs)
