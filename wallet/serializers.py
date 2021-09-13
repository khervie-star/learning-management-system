from rest_framework import serializers
from wallet.models import Payment, Wallet

from course.models import Course


class VerifyPaymentSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField()
    payment_reference = serializers.CharField()


class InitiatePaymentSerializer(serializers.ModelSerializer):
    course_slug = serializers.CharField(write_only=True)
    course_to_enroll = serializers.SlugRelatedField(
        slug_field="course_payment", read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = (
            'verified', 'reference', 'course_to_enroll', "amount"
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class WalletSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
