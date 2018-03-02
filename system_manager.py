from models.monitor import Monitor


class SystemManager:
    class __SystemManager:
        def __init__(self):
            self.monitor = Monitor()

    instance = None

    def __init__(self, arg):
        if not SystemManager.instance:
            SystemManager.instance = SystemManager.__SystemManager()
        else:
            SystemManager.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)
