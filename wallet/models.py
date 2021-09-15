import secrets
from django.db import models

from instructor.models import Instructor
from course.models import Course
from student.models import Profile
from wallet.paystack import PayStack


class Wallet(models.Model):
    wallet_owner = models.ForeignKey(
        Instructor, null=True, on_delete=models.CASCADE, related_name="my_wallet")
    balance = models.FloatField(default=0.00)
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
    auth_student = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    course_to_enroll = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="course_payment")
    amount = models.PositiveIntegerField(null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)

    transaction_ref = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        while not self.reference:
            ref = secrets.token_urlsafe(50)
            object = Payment.objects.filter(reference=ref)
            if not object:
                self.reference = ref
        super(Payment, self).save(*args, **kwargs)

    @staticmethod
    def get_amount(self):
        return self.amount * 100

    def verify_payment(self):
        paystack_object = PayStack()
        status, result = paystack_object.verify_payment(self.transaction_ref)
        if status:
            # remeber that the paystack currency is always multiplied by 100 to convert to the least currency unit...
            if result['amount']/100 >= self.amount:
                self.verified = True
            self.save()
            if self.verified:
                return True, result
            else:
                self.verified = False
        return False, result


class Transfers(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.PROTECT, related_name="my_transfers")
    bank_type = models.CharField(max_length=500, null=True, blank=True)
    account_number = models.PositiveIntegerField()
    account_name = models.CharField(max_length=200, null=True, blank=True)
    # change this to not nullable and not blank
    amount = models.PositiveIntegerField(null=True, blank=True)
    bank_code = models.PositiveIntegerField(null=True, blank=True)
    bank_name = models.CharField(max_length=2000, null=True, blank=True)
    bank_type = models.CharField(max_length=2000, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    recipient_code = models.CharField(max_length=1000, null=True, blank=True)
    payment_account_resolved = models.BooleanField(default=False)
    # change this to not nullable and not blank
    transfer_reference = models.CharField(max_length=500, null=True, blank=True)
    tranferred = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Transfers"
