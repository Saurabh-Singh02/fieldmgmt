from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Job, Notification, CustomUser

@receiver(post_save, sender=Job)
def notify_managers_on_job_update(sender, instance, created, **kwargs):
    """
    Send notifications to all managers when a job is updated
    """
    if not created:  # Only for updates, not creations
        # Get all managers
        managers = CustomUser.objects.filter(role='manager')
        
        for manager in managers:
            # Create notification for each manager
            Notification.objects.create(
                user=manager,
                notification_type='job_updated',
                title=f'Job Updated: {instance.job_id}',
                message=f'''
Job "{instance.title}" has been updated by {instance.updated_by.get_full_name() if instance.updated_by else "System"}.

Client: {instance.client.name}
Status: {instance.get_status_display()}
Priority: {instance.get_priority_display()}
Last Updated: {instance.last_updated.strftime("%Y-%m-%d %H:%M")}

Click to view details.
                ''',
                related_object_type='job',
                related_object_id=instance.id
            )