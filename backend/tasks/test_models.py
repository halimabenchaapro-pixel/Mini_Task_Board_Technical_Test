"""
Comprehensive tests for Task model
Tests all model methods, properties, and database constraints
"""
from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from .models import Task


class TaskModelTest(TestCase):
    """Test suite for Task model"""

    def setUp(self):
        """Set up test data"""
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': Task.Status.BACKLOG,
            'priority': Task.Priority.MEDIUM,
            'due_date': date.today() + timedelta(days=7)
        }

    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields populated"""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, Task.Status.BACKLOG)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_create_task_with_minimal_fields(self):
        """Test creating a task with only required fields"""
        task = Task.objects.create(title='Minimal Task')
        self.assertEqual(task.title, 'Minimal Task')
        self.assertEqual(task.status, Task.Status.BACKLOG)  # Default
        self.assertEqual(task.priority, Task.Priority.MEDIUM)  # Default
        self.assertIsNone(task.description)
        self.assertIsNone(task.due_date)

    def test_task_str_method(self):
        """Test __str__ method returns task title"""
        task = Task.objects.create(title='String Test Task')
        self.assertEqual(str(task), 'String Test Task')

    def test_task_status_choices(self):
        """Test all status choices are valid"""
        statuses = [Task.Status.BACKLOG, Task.Status.IN_PROGRESS, Task.Status.DONE]
        for status in statuses:
            task = Task.objects.create(
                title=f'Task with {status}',
                status=status
            )
            self.assertEqual(task.status, status)
            task.delete()

    def test_task_priority_choices(self):
        """Test all priority choices are valid"""
        priorities = [Task.Priority.LOW, Task.Priority.MEDIUM, Task.Priority.HIGH]
        for priority in priorities:
            task = Task.objects.create(
                title=f'Task with {priority}',
                priority=priority
            )
            self.assertEqual(task.priority, priority)
            task.delete()

    def test_task_default_status(self):
        """Test task defaults to BACKLOG status"""
        task = Task.objects.create(title='Default Status Task')
        self.assertEqual(task.status, Task.Status.BACKLOG)

    def test_task_default_priority(self):
        """Test task defaults to MEDIUM priority"""
        task = Task.objects.create(title='Default Priority Task')
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_task_title_max_length(self):
        """Test title field max length constraint"""
        long_title = 'a' * 200
        task = Task.objects.create(title=long_title)
        self.assertEqual(len(task.title), 200)

    def test_task_timestamps(self):
        """Test created_at and updated_at timestamps"""
        task = Task.objects.create(title='Timestamp Test')
        created_at = task.created_at
        updated_at = task.updated_at

        # Timestamps should be set
        self.assertIsNotNone(created_at)
        self.assertIsNotNone(updated_at)

        # Update the task
        task.title = 'Updated Title'
        task.save()

        # created_at should not change
        self.assertEqual(task.created_at, created_at)
        # updated_at should change
        self.assertGreater(task.updated_at, updated_at)

    def test_task_due_date_optional(self):
        """Test due_date is optional"""
        task = Task.objects.create(title='No Due Date Task')
        self.assertIsNone(task.due_date)

    def test_task_due_date_set(self):
        """Test setting a due date"""
        future_date = date.today() + timedelta(days=30)
        task = Task.objects.create(
            title='Due Date Task',
            due_date=future_date
        )
        self.assertEqual(task.due_date, future_date)

    def test_task_description_optional(self):
        """Test description is optional"""
        task = Task.objects.create(title='No Description Task')
        self.assertIsNone(task.description)

    def test_task_description_can_be_long(self):
        """Test description can store long text"""
        long_description = 'a' * 1000
        task = Task.objects.create(
            title='Long Description Task',
            description=long_description
        )
        self.assertEqual(len(task.description), 1000)

    def test_task_ordering(self):
        """Test tasks are ordered by creation date (newest first)"""
        task1 = Task.objects.create(title='First Task')
        task2 = Task.objects.create(title='Second Task')
        task3 = Task.objects.create(title='Third Task')

        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0].id, task3.id)
        self.assertEqual(tasks[1].id, task2.id)
        self.assertEqual(tasks[2].id, task1.id)

    def test_task_update_status(self):
        """Test updating task status"""
        task = Task.objects.create(title='Status Update Task')
        self.assertEqual(task.status, Task.Status.BACKLOG)

        task.status = Task.Status.IN_PROGRESS
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

        task.status = Task.Status.DONE
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)

    def test_task_update_priority(self):
        """Test updating task priority"""
        task = Task.objects.create(title='Priority Update Task')
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

        task.priority = Task.Priority.HIGH
        task.save()
        task.refresh_from_db()
        self.assertEqual(task.priority, Task.Priority.HIGH)

    def test_multiple_tasks_creation(self):
        """Test creating multiple tasks"""
        tasks_data = [
            {'title': f'Task {i}', 'priority': Task.Priority.HIGH}
            for i in range(10)
        ]

        for data in tasks_data:
            Task.objects.create(**data)

        self.assertEqual(Task.objects.count(), 10)
        self.assertEqual(Task.objects.filter(priority=Task.Priority.HIGH).count(), 10)

    def test_task_filter_by_status(self):
        """Test filtering tasks by status"""
        Task.objects.create(title='Backlog Task 1', status=Task.Status.BACKLOG)
        Task.objects.create(title='Backlog Task 2', status=Task.Status.BACKLOG)
        Task.objects.create(title='In Progress Task', status=Task.Status.IN_PROGRESS)
        Task.objects.create(title='Done Task', status=Task.Status.DONE)

        backlog_tasks = Task.objects.filter(status=Task.Status.BACKLOG)
        self.assertEqual(backlog_tasks.count(), 2)

    def test_task_filter_by_priority(self):
        """Test filtering tasks by priority"""
        Task.objects.create(title='High Priority 1', priority=Task.Priority.HIGH)
        Task.objects.create(title='High Priority 2', priority=Task.Priority.HIGH)
        Task.objects.create(title='Medium Priority', priority=Task.Priority.MEDIUM)
        Task.objects.create(title='Low Priority', priority=Task.Priority.LOW)

        high_priority_tasks = Task.objects.filter(priority=Task.Priority.HIGH)
        self.assertEqual(high_priority_tasks.count(), 2)
