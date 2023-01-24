from rest_framework import serializers

from .models import *

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    user_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','FirstName','LastName','DOB','Btype','typee','Place','email','phone']


class RequestSerializer(serializers.ModelSerializer):
    collectedQty = serializers.ReadOnlyField()
    remainingQty = serializers.ReadOnlyField()
    class Meta:
        model = Request
        fields = ['id','Btype','quantity','Status','user','send_at','user','collectedQty','remainingQty']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data

        return data

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['donor'] is not None:
            data['donor'] = UserSerializer(
                User.objects.get(pk=data['donor'])).data
        if data['request'] is not None:
            data['request'] = RequestSerializer(
                Request.objects.get(pk=data['request'])).data

        return data
