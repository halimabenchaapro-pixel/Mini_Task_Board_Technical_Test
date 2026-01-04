from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_status(self, value):
        """Validate status is a valid choice"""
        if value not in [choice[0] for choice in Task.Status.choices]:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join([choice[0] for choice in Task.Status.choices])}"
            )
        return value

    def validate_priority(self, value):
        """Validate priority is a valid choice"""
        if value not in [choice[0] for choice in Task.Priority.choices]:
            raise serializers.ValidationError(
                f"Invalid priority. Must be one of: {', '.join([choice[0] for choice in Task.Priority.choices])}"
            )
        return value
