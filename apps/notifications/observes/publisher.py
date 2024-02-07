from typing import List

from apps.notifications.observes.notification_abstracts import (
    NotificationSubscriberAbstract,
)


class NotificationPublisher:
    def __init__(self):
        self._subscribers: List[NotificationSubscriberAbstract] = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def unsubscribe_all(self):
        self._subscribers.clear()

    def notify(self, who: str, message: str):
        for subscriber in self._subscribers:
            subscriber.update(who, message)
