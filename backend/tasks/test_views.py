"""
Comprehensive tests for Task API views
Tests all ViewSet actions, custom endpoints, filtering, pagination, and error handling
"""
from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Task


class TaskViewSetTest(TestCase):
    """Test suite for TaskViewSet"""

    def setUp(self):
        """Set up test client and sample data"""
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY=settings.API_KEY)

        # Create test tasks
        self.task1 = Task.objects.create(
            title="Task 1",
            description="Description 1",
            status=Task.Status.BACKLOG,
            priority=Task.Priority.HIGH
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            description="Description 2",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM
        )
        self.task3 = Task.objects.create(
            title="Task 3",
            description="Description 3",
            status=Task.Status.DONE,
            priority=Task.Priority.LOW
        )

    def test_list_tasks(self):
        """Test GET /api/tasks/ returns all tasks"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)

    def test_retrieve_task(self):
        """Test GET /api/tasks/{id}/ returns single task"""
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_create_task(self):
        """Test POST /api/tasks/ creates new task"""
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'BACKLOG',
            'priority': 'HIGH'
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Task created successfully')
        self.assertEqual(response.data['data']['title'], 'New Task')

    def test_update_task_full(self):
        """Test PUT /api/tasks/{id}/ updates entire task"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'DONE',
            'priority': 'LOW'
        }
        response = self.client.put(f'/api/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Task updated successfully')

    def test_update_task_partial(self):
        """Test PATCH /api/tasks/{id}/ partially updates task"""
        data = {'status': 'DONE'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['status'], 'DONE')

    def test_delete_task(self):
        """Test DELETE /api/tasks/{id}/ deletes task"""
        task_count = Task.objects.count()
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Task deleted successfully')
        self.assertEqual(Task.objects.count(), task_count - 1)

    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        response = self.client.get('/api/tasks/?status=BACKLOG')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data['results']:
            self.assertEqual(task['status'], 'BACKLOG')

    def test_filter_by_priority(self):
        """Test filtering tasks by priority"""
        response = self.client.get('/api/tasks/?priority=HIGH')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data['results']:
            self.assertEqual(task['priority'], 'HIGH')

    def test_search_tasks(self):
        """Test searching tasks by title/description"""
        response = self.client.get('/api/tasks/?search=Task 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_ordering_by_created_at(self):
        """Test ordering tasks by created_at"""
        response = self.client.get('/api/tasks/?ordering=-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        if len(results) >= 2:
            self.assertGreaterEqual(results[0]['created_at'], results[1]['created_at'])

    def test_pagination(self):
        """Test pagination works correctly"""
        # Create more tasks to test pagination
        for i in range(15):
            Task.objects.create(title=f'Pagination Task {i}')

        response = self.client.get('/api/tasks/?page=1&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 10)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)

    def test_bulk_update_status(self):
        """Test POST /api/tasks/bulk_update_status/ updates multiple tasks"""
        data = {
            'task_ids': [self.task1.id, self.task2.id],
            'status': 'DONE'
        }
        response = self.client.post('/api/tasks/bulk_update_status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['updated_count'], 2)

        # Verify tasks were updated
        self.task1.refresh_from_db()
        self.task2.refresh_from_db()
        self.assertEqual(self.task1.status, Task.Status.DONE)
        self.assertEqual(self.task2.status, Task.Status.DONE)

    def test_bulk_update_status_missing_params(self):
        """Test bulk update fails with missing parameters"""
        data = {'task_ids': [self.task1.id]}
        response = self.client.post('/api/tasks/bulk_update_status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_update_status_invalid_status(self):
        """Test bulk update fails with invalid status"""
        data = {
            'task_ids': [self.task1.id],
            'status': 'INVALID'
        }
        response = self.client.post('/api/tasks/bulk_update_status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_statistics_endpoint(self):
        """Test GET /api/tasks/statistics/ returns correct statistics"""
        response = self.client.get('/api/tasks/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check structure
        self.assertIn('total', response.data)
        self.assertIn('by_status', response.data)
        self.assertIn('by_priority', response.data)

        # Check values
        self.assertEqual(response.data['total'], Task.objects.count())
        self.assertEqual(response.data['by_status']['backlog'],
                        Task.objects.filter(status='BACKLOG').count())

    def test_filter_by_due_date_range(self):
        """Test filtering by due_date range"""
        # Create tasks with due dates
        today = date.today()
        Task.objects.create(
            title='Due Today',
            due_date=today
        )
        Task.objects.create(
            title='Due Tomorrow',
            due_date=today + timedelta(days=1)
        )

        response = self.client.get(
            f'/api/tasks/?due_date_from={today}&due_date_to={today}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_overdue_tasks(self):
        """Test filtering overdue tasks"""
        # Create an overdue task
        Task.objects.create(
            title='Overdue Task',
            due_date=date.today() - timedelta(days=1),
            status=Task.Status.BACKLOG
        )

        response = self.client.get('/api/tasks/?overdue=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task_validation_error(self):
        """Test creating task with invalid data returns error"""
        data = {'description': 'No title'}
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_task(self):
        """Test updating non-existent task returns 404"""
        data = {'title': 'Updated'}
        response = self.client.patch('/api/tasks/9999/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task returns 404"""
        response = self.client.delete('/api/tasks/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_nonexistent_task(self):
        """Test retrieving non-existent task returns 404"""
        response = self.client.get('/api/tasks/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_access(self):
        """Test accessing API without credentials"""
        client = APIClient()
        response = client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_api_key(self):
        """Test accessing API with invalid credentials"""
        client = APIClient()
        client.credentials(HTTP_X_API_KEY='invalid-key')
        response = client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_multiple_filters_combined(self):
        """Test combining multiple filters"""
        response = self.client.get('/api/tasks/?status=BACKLOG&priority=HIGH')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data['results']:
            self.assertEqual(task['status'], 'BACKLOG')
            self.assertEqual(task['priority'], 'HIGH')

    def test_search_and_filter_combined(self):
        """Test combining search with filters"""
        response = self.client.get('/api/tasks/?search=Task&status=BACKLOG')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_size_parameter(self):
        """Test page_size parameter controls pagination"""
        response = self.client.get('/api/tasks/?page_size=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']), 2)

    def test_max_page_size_limit(self):
        """Test page_size is capped at max_page_size"""
        response = self.client.get('/api/tasks/?page_size=1000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be limited to 100 (max_page_size)
        self.assertLessEqual(len(response.data['results']), 100)
