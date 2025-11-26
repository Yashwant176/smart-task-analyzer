from rest_framework import serializers

class InputTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=300)
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(required=False, min_value=0.0)
    importance = serializers.IntegerField(required=False, min_value=1, max_value=10)
    dependencies = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    def validate(self, data):
       
        data.setdefault('estimated_hours', 1.0)
        data.setdefault('importance', 5)
        data.setdefault('dependencies', [])
        return data
