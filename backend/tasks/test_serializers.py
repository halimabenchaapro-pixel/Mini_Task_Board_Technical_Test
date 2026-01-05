"""
Comprehensive tests for Task serializers
Tests all validation logic and serialization/deserialization
"""
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta
from .models import Task
from .serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    """Test suite for TaskSerializer"""

    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'BACKLOG',
            'priority': 'MEDIUM',
            'due_date': str(date.today() + timedelta(days=7))
        }

        self.task = Task.objects.create(
            title='Existing Task',
            description='Existing Description',
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH
        )

    def test_serialize_task(self):
        """Test serializing a task instance"""
        serializer = TaskSerializer(self.task)
        data = serializer.data

        self.assertEqual(data['title'], 'Existing Task')
        self.assertEqual(data['description'], 'Existing Description')
        self.assertEqual(data['status'], 'IN_PROGRESS')
        self.assertEqual(data['priority'], 'HIGH')
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

    def test_deserialize_valid_data(self):
        """Test deserializing valid data"""
        serializer = TaskSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()

        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, Task.Status.BACKLOG)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_validate_title_required(self):
        """Test title is required"""
        data = self.valid_data.copy()
        del data['title']

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_title_not_empty(self):
        """Test title cannot be empty"""
        data = self.valid_data.copy()
        data['title'] = ''

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_title_whitespace_only(self):
        """Test title cannot be whitespace only"""
        data = self.valid_data.copy()
        data['title'] = '   '

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_validate_title_strips_whitespace(self):
        """Test title whitespace is stripped"""
        data = self.valid_data.copy()
        data['title'] = '  Trimmed Task  '

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, 'Trimmed Task')

    def test_validate_status_valid_choices(self):
        """Test status accepts valid choices"""
        valid_statuses = ['BACKLOG', 'IN_PROGRESS', 'DONE']

        for status in valid_statuses:
            data = self.valid_data.copy()
            data['status'] = status

            serializer = TaskSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Status {status} should be valid")

    def test_validate_status_invalid_choice(self):
        """Test status rejects invalid choices"""
        data = self.valid_data.copy()
        data['status'] = 'INVALID_STATUS'

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_validate_priority_valid_choices(self):
        """Test priority accepts valid choices"""
        valid_priorities = ['LOW', 'MEDIUM', 'HIGH']

        for priority in valid_priorities:
            data = self.valid_data.copy()
            data['priority'] = priority

            serializer = TaskSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"Priority {priority} should be valid")

    def test_validate_priority_invalid_choice(self):
        """Test priority rejects invalid choices"""
        data = self.valid_data.copy()
        data['priority'] = 'INVALID_PRIORITY'

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('priority', serializer.errors)

    def test_description_optional(self):
        """Test description is optional"""
        data = self.valid_data.copy()
        del data['description']

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_description_can_be_null(self):
        """Test description can be null"""
        data = self.valid_data.copy()
        data['description'] = None

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_due_date_optional(self):
        """Test due_date is optional"""
        data = self.valid_data.copy()
        del data['due_date']

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_due_date_valid_format(self):
        """Test due_date accepts valid date format"""
        data = self.valid_data.copy()
        data['due_date'] = '2026-12-31'

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_due_date_invalid_format(self):
        """Test due_date rejects invalid date format"""
        data = self.valid_data.copy()
        data['due_date'] = 'invalid-date'

        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_date', serializer.errors)

    def test_read_only_fields(self):
        """Test id, created_at, updated_at are read-only"""
        data = self.valid_data.copy()
        data['id'] = 999
        data['created_at'] = '2020-01-01T00:00:00Z'
        data['updated_at'] = '2020-01-01T00:00:00Z'

        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()

        # Read-only fields should be auto-generated, not from input
        self.assertNotEqual(task.id, 999)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_update_task(self):
        """Test updating a task via serializer"""
        update_data = {
            'title': 'Updated Title',
            'status': 'DONE'
        }

        serializer = TaskSerializer(self.task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()

        self.assertEqual(updated_task.title, 'Updated Title')
        self.assertEqual(updated_task.status, Task.Status.DONE)

    def test_partial_update(self):
        """Test partial update only changes specified fields"""
        original_description = self.task.description
        update_data = {'priority': 'LOW'}

        serializer = TaskSerializer(self.task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()

        self.assertEqual(updated_task.priority, Task.Priority.LOW)
        self.assertEqual(updated_task.description, original_description)

    def test_serialize_multiple_tasks(self):
        """Test serializing multiple tasks"""
        tasks = [
            Task.objects.create(title=f'Task {i}', priority=Task.Priority.HIGH)
            for i in range(5)
        ]

        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(len(serializer.data), 5)

    def test_all_fields_included(self):
        """Test all expected fields are included in serialized data"""
        serializer = TaskSerializer(self.task)
        expected_fields = [
            'id', 'title', 'description', 'status',
            'priority', 'due_date', 'created_at', 'updated_at'
        ]

        for field in expected_fields:
            self.assertIn(field, serializer.data)

    def test_serializer_handles_all_status_values(self):
        """Test serializer correctly handles all status enum values"""
        for status_value, status_label in Task.Status.choices:
            task = Task.objects.create(
                title=f'Task with {status_label}',
                status=status_value
            )
            serializer = TaskSerializer(task)
            self.assertEqual(serializer.data['status'], status_value)
            task.delete()

    def test_serializer_handles_all_priority_values(self):
        """Test serializer correctly handles all priority enum values"""
        for priority_value, priority_label in Task.Priority.choices:
            task = Task.objects.create(
                title=f'Task with {priority_label}',
                priority=priority_value
            )
            serializer = TaskSerializer(task)
            self.assertEqual(serializer.data['priority'], priority_value)
            task.delete()
