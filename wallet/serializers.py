from rest_framework import serializers
from wallet.models import Payment


class VerifyPaymentSerializer(serializers.Serializer):
    transaction_refernce = serializers.CharField()


class InitiatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = (
            'verified', 'reference'
        )
