from rest_framework import serializers


class VerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=20)
