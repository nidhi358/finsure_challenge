from rest_framework import serializers

from .models import Lender


class LenderSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=1000)
  code = serializers.CharField(max_length=3)
  upfront_comm_rate = serializers.DecimalField(max_digits =5, decimal_places=2, max_value=100, min_value=0)
  trail_comm_rate = serializers.DecimalField(max_digits =5, decimal_places=2, max_value=100, min_value=0)
  is_active = serializers.BooleanField()


  def create(self, validated_data):
    # Once the request data has been validated, we can create a lender item instance in the database
    return Lender.objects.create(
        name = validated_data.get('name'),
        code = validated_data.get('code'),
        upfront_comm_rate = validated_data.get('upfront_comm_rate'),
        trail_comm_rate = validated_data.get('trail_comm_rate'),
        is_active = validated_data.get('is_active'),
    )


  def update(self, instance, validated_data):
     # Once the request data has been validated, we can update the lender item instance in the database
    instance.name = validated_data.get('name', instance.name)
    instance.code = validated_data.get('code', instance.code)
    instance.upfront_comm_rate = validated_data.get('upfront_comm_rate', instance.upfront_comm_rate)
    instance.trail_comm_rate = validated_data.get('trail_comm_rate', instance.trail_comm_rate)
    instance.is_active = validated_data.get('is_active', instance.is_active)
    instance.save()
    return instance

  class Meta:
    model = Lender
    fields = (
      'id',
      'name',
      'code',
      'upfront_comm_rate',
      'trail_comm_rate',
      'is_active'
    )