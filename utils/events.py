class Event:
    subscribers = []

    @classmethod
    def subscribe(cls, instance):
        cls.subscribers.append(instance)

    @classmethod
    def unsubscribe(cls, instance):
        pass
