# refease/referral_app/serializers.py

from rest_framework import serializers
from .models import User

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class CodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite_code', 'referrals']

    def get_referrals(self, obj):
        return [user.phone_number for user in obj.referrals.all()]

class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField()
