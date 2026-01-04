from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Task model with:
    - Colored priority badges
    - Status indicators
    - Bulk actions
    - Advanced filtering
    - Export capabilities
    """

    list_display = [
        'title_display',
        'status_display',
        'priority_display',
        'due_date',
        'created_at',
        'days_since_creation'
    ]

    list_filter = [
        'status',
        'priority',
        'created_at',
        'due_date',
        ('due_date', admin.EmptyFieldListFilter),
    ]

    search_fields = ['title', 'description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    # Read-only fields for audit trail
    readonly_fields = ['created_at', 'updated_at', 'days_since_creation']

    # Fields to show in the form
    fields = [
        'title',
        'description',
        'status',
        'priority',
        'due_date',
        'created_at',
        'updated_at',
    ]

    # Enable bulk editing
    list_editable = []

    # Number of items per page
    list_per_page = 25

    # Actions
    actions = [
        'mark_as_in_progress',
        'mark_as_done',
        'mark_as_backlog',
        'set_priority_high',
        'set_priority_medium',
        'set_priority_low',
    ]

    def title_display(self, obj):
        """Display title with icon based on status"""
        icons = {
            'BACKLOG': '📋',
            'IN_PROGRESS': '⏳',
            'DONE': '✅',
        }
        return format_html(
            '<strong>{} {}</strong>',
            icons.get(obj.status, ''),
            obj.title
        )
    title_display.short_description = 'Task Title'

    def status_display(self, obj):
        """Display status with colored badge"""
        colors = {
            'BACKLOG': '#6c757d',
            'IN_PROGRESS': '#007bff',
            'DONE': '#28a745',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'

    def priority_display(self, obj):
        """Display priority with colored badge"""
        colors = {
            'LOW': '#28a745',
            'MEDIUM': '#ffc107',
            'HIGH': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.get_priority_display()
        )
    priority_display.short_description = 'Priority'
    priority_display.admin_order_field = 'priority'

    def days_since_creation(self, obj):
        """Calculate days since task was created"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        days = delta.days
        if days == 0:
            return "Today"
        elif days == 1:
            return "Yesterday"
        else:
            return f"{days} days ago"
    days_since_creation.short_description = 'Age'

    # Bulk Actions
    def mark_as_in_progress(self, request, queryset):
        """Bulk action to mark tasks as In Progress"""
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f'{updated} task(s) marked as In Progress.')
    mark_as_in_progress.short_description = "Mark selected as In Progress"

    def mark_as_done(self, request, queryset):
        """Bulk action to mark tasks as Done"""
        updated = queryset.update(status='DONE')
        self.message_user(request, f'{updated} task(s) marked as Done.')
    mark_as_done.short_description = "Mark selected as Done"

    def mark_as_backlog(self, request, queryset):
        """Bulk action to mark tasks as Backlog"""
        updated = queryset.update(status='BACKLOG')
        self.message_user(request, f'{updated} task(s) moved to Backlog.')
    mark_as_backlog.short_description = "Move selected to Backlog"

    def set_priority_high(self, request, queryset):
        """Bulk action to set priority to High"""
        updated = queryset.update(priority='HIGH')
        self.message_user(request, f'{updated} task(s) set to High priority.')
    set_priority_high.short_description = "Set priority to High"

    def set_priority_medium(self, request, queryset):
        """Bulk action to set priority to Medium"""
        updated = queryset.update(priority='MEDIUM')
        self.message_user(request, f'{updated} task(s) set to Medium priority.')
    set_priority_medium.short_description = "Set priority to Medium"

    def set_priority_low(self, request, queryset):
        """Bulk action to set priority to Low"""
        updated = queryset.update(priority='LOW')
        self.message_user(request, f'{updated} task(s) set to Low priority.')
    set_priority_low.short_description = "Set priority to Low"

    def changelist_view(self, request, extra_context=None):
        """Add custom statistics to the changelist view"""
        extra_context = extra_context or {}

        # Calculate statistics
        extra_context['total_tasks'] = Task.objects.count()
        extra_context['backlog_count'] = Task.objects.filter(status='BACKLOG').count()
        extra_context['in_progress_count'] = Task.objects.filter(status='IN_PROGRESS').count()
        extra_context['done_count'] = Task.objects.filter(status='DONE').count()
        extra_context['high_priority_count'] = Task.objects.filter(priority='HIGH').count()

        return super().changelist_view(request, extra_context=extra_context)
