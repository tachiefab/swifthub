from django.urls import path
from .views import NotificationListView, MarkNotificationAsRead

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name="notification-list"),
    path('<int:notification_id>/read/', MarkNotificationAsRead.as_view(), name="mark_as_read"),
]
