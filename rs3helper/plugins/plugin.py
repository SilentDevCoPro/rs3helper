class Plugin:
    def __init__(self, name: str):
        self.name = name
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def update(self):
        pass  # This method should be overridden by subclasses

    def stop(self):
        pass  # This method should be overridden by subclasses
