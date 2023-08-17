from rest_framework import serializers
from .models import Lender

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
class SaveFileSerializer(serializers.Serializer):
    
    class Meta:
        model = Lender
        fields = "__all__"