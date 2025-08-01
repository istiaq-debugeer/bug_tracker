from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
