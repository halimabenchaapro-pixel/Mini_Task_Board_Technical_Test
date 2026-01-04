from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer
import logging

logger = logging.getLogger(__name__)


class TaskPagination(PageNumberPagination):
    """
    Custom pagination class for tasks
    Allows clients to control page size within limits
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    """
    Enhanced ViewSet for Task CRUD operations with:
    - Pagination support
    - Filtering and search
    - Custom bulk actions
    - Proper error handling
    - Request logging
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Enhanced queryset with filtering support
        Supports filtering by status, priority, and date ranges
        """
        queryset = Task.objects.all()

        # Filter by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)

        # Filter by priority
        priority_param = self.request.query_params.get('priority', None)
        if priority_param:
            queryset = queryset.filter(priority=priority_param)

        # Filter by due date range
        due_date_from = self.request.query_params.get('due_date_from', None)
        due_date_to = self.request.query_params.get('due_date_to', None)

        if due_date_from:
            queryset = queryset.filter(due_date__gte=due_date_from)
        if due_date_to:
            queryset = queryset.filter(due_date__lte=due_date_to)

        # Filter overdue tasks
        overdue = self.request.query_params.get('overdue', None)
        if overdue == 'true':
            from django.utils import timezone
            queryset = queryset.filter(
                due_date__lt=timezone.now().date()
            ).exclude(status='DONE')

        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new task with validation and logging"""
        logger.info(f"Creating new task from IP: {request.META.get('REMOTE_ADDR')}")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        logger.info(f"Task created: {serializer.data['id']} - {serializer.data['title']}")

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'success': True,
                'message': 'Task created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Update an existing task with validation and logging"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        logger.info(f"Updating task {instance.id}: {instance.title}")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        logger.info(f"Task updated: {instance.id}")

        return Response({
            'success': True,
            'message': 'Task updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """Delete a task with logging"""
        instance = self.get_object()
        task_id = instance.id
        task_title = instance.title

        logger.info(f"Deleting task {task_id}: {task_title}")

        self.perform_destroy(instance)

        logger.info(f"Task deleted: {task_id}")

        return Response(
            {
                'success': True,
                'message': 'Task deleted successfully'
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def bulk_update_status(self, request):
        """
        Bulk update status for multiple tasks
        POST /api/tasks/bulk_update_status/
        Body: {"task_ids": [1, 2, 3], "status": "DONE"}
        """
        task_ids = request.data.get('task_ids', [])
        new_status = request.data.get('status')

        if not task_ids or not new_status:
            return Response(
                {'error': 'task_ids and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in dict(Task.Status.choices):
            return Response(
                {'error': 'Invalid status value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated = Task.objects.filter(id__in=task_ids).update(status=new_status)

        logger.info(f"Bulk updated {updated} tasks to status {new_status}")

        return Response({
            'success': True,
            'message': f'{updated} task(s) updated successfully',
            'updated_count': updated
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get task statistics
        GET /api/tasks/statistics/
        """
        from django.db.models import Count

        stats = {
            'total': Task.objects.count(),
            'by_status': {
                'backlog': Task.objects.filter(status='BACKLOG').count(),
                'in_progress': Task.objects.filter(status='IN_PROGRESS').count(),
                'done': Task.objects.filter(status='DONE').count(),
            },
            'by_priority': {
                'low': Task.objects.filter(priority='LOW').count(),
                'medium': Task.objects.filter(priority='MEDIUM').count(),
                'high': Task.objects.filter(priority='HIGH').count(),
            }
        }

        return Response(stats)
