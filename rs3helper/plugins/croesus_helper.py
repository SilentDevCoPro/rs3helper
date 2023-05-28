from rs3helper.plugins.plugin import Plugin


class CroesusHelper(Plugin):
    def __init__(self):
        super().__init__("Croesus Helper")

    def update(self):
        if self.detect_boss_encounter():
            self.start_timers()

    def detect_boss_encounter(self):
        # TODO: Implement boss encounter detection
        pass

    def start_timers(self):
        # TODO: Implement timers for boss abilities
        pass
