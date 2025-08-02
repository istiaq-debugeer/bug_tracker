from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ActivityLog


def notify_project(projects_id, message_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"projects_{projects_id}",
        {
            "type": "send_notification",
            "message": message_data,
        },
    )


def notify_users(user_ids, message_data):
    channel_layer = get_channel_layer()
    for user_id in user_ids:
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_notification",
                "message": message_data,
            },
        )


def log_and_notify(project_id, user, event, bug=None, message=""):
    ActivityLog.objects.create(
        event=event,
        bug=bug,
        project_id=project_id,
        user=user,
        message=message
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"project_{project_id}",  # group name
        {
            "type": "send_notification",
            "message": {
                "event": event,
                "bug_id": bug.id if bug else None,
                "message": message,
            },
        },
    )