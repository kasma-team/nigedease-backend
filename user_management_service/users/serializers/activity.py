from rest_framework import serializers

class ActivityLogSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField()
    user_email = serializers.CharField(read_only=True)
    action = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True) 