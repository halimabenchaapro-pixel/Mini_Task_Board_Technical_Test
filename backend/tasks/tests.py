from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


class TaskAPITestCase(TestCase):
    """Test suite for Task API endpoints"""

    def setUp(self):
        """Set up test client and sample data"""
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY=settings.API_KEY)

        # Create a sample task
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            status=Task.Status.BACKLOG,
            priority=Task.Priority.MEDIUM
        )

    def test_create_task_validation(self):
        """Test creating a task with required title validation"""
        # Test with valid data
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "BACKLOG",
            "priority": "HIGH"
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Task")

        # Test with empty title (should fail)
        data_no_title = {
            "title": "",
            "description": "Description"
        }
        response = self.client.post('/api/tasks/', data_no_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with missing title (should fail)
        data_missing_title = {
            "description": "Description only"
        }
        response = self.client.post('/api/tasks/', data_missing_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_status(self):
        """Test updating a task's status"""
        # Update status from BACKLOG to IN_PROGRESS
        data = {
            "status": "IN_PROGRESS"
        }
        response = self.client.patch(
            f'/api/tasks/{self.task.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "IN_PROGRESS")

        # Verify the task was updated in the database
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)

        # Test invalid status
        data_invalid = {
            "status": "INVALID_STATUS"
        }
        response = self.client.patch(
            f'/api/tasks/{self.task.id}/',
            data_invalid,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task(self):
        """Test deleting a task"""
        # Get initial count
        initial_count = Task.objects.count()

        # Delete the task
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify task was deleted
        self.assertEqual(Task.objects.count(), initial_count - 1)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

        # Test deleting non-existent task
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_tasks(self):
        """Test listing all tasks"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_task(self):
        """Test retrieving a single task"""
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_api_key_authentication(self):
        """Test that API key authentication is required"""
        # Create a client without API key
        client_no_auth = APIClient()

        response = client_no_auth.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with invalid API key
        client_invalid_key = APIClient()
        client_invalid_key.credentials(HTTP_X_API_KEY='invalid-key')
        response = client_invalid_key.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
