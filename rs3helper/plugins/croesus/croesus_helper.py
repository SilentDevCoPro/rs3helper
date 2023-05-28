from rs3helper.plugins.plugin import Plugin
from threading import Timer


class CroesusHelper(Plugin):
    abilities = ["Red Spore Bomb", "Fairy Ring", "Slime Mould", "Yellow Spore Bomb",
                 "Hard Fungus Fall (Stun)", "Sticky Fungus", "Green Spore Bomb", "Blue Spore Bomb",
                 "Sticky Fungus & Energy Fungus"]
    intervals = [14, 23, 38, 51, 63, 72, 86, 97, 111, 123, 134, 143]  # time intervals in seconds

    def __init__(self):
        super().__init__("Croesus Helper")
        self.is_boss_encounter_tracking = False
        self.ability_timers = {ability: None for ability in self.abilities}

    def update(self):
        if self.detect_boss_encounter() and not self.is_boss_encounter_tracking:
            self.start_timers()
            self.is_boss_encounter_tracking = True
        elif not self.detect_boss_encounter() and self.is_boss_encounter_tracking:
            self.stop()

    def detect_boss_encounter(self):
        # TODO: Implement boss encounter detection
        return True #For thesting

    def start_timers(self):
        for i, ability in enumerate(self.abilities):
            self.set_ability_timer(ability, self.intervals[i])

    def stop(self):
        self.is_boss_encounter_tracking = False
        for timer in self.ability_timers.values():
            if timer is not None:
                timer.cancel()

    def set_ability_timer(self, ability, interval):
        method_name = ability.replace(' ', '_').lower()
        self.ability_timers[ability] = Timer(interval, getattr(self, method_name))
        self.ability_timers[ability].start()

    # define methods for each ability
    def red_spore_bomb(self):
        print("Boss used Red Spore Bomb!")
        self.set_ability_timer("Red Spore Bomb", 14)

    def fairy_ring(self):
        print("Boss used Fairy Ring!")
        self.set_ability_timer("Fairy Ring", 23)

    def slime_mould(self):
        print("Boss used Slime Mould!")
        self.set_ability_timer("Slime Mould", 38)

    def yellow_spore_bomb(self):
        print("Boss used Yellow Spore Bomb!")
        self.set_ability_timer("Yellow Spore Bomb", 51)

    def hard_fungus_fall_stun(self):
        print("Boss used Hard Fungus Fall (Stun)!")
        self.set_ability_timer("Hard Fungus Fall (Stun)", 63)

    def sticky_fungus(self):
        print("Boss used Sticky Fungus!")
        self.set_ability_timer("Sticky Fungus", 72)

    def green_spore_bomb(self):
        print("Boss used Green Spore Bomb!")
        self.set_ability_timer("Green Spore Bomb", 86)

    def blue_spore_bomb(self):
        print("Boss used Blue Spore Bomb!")
        self.set_ability_timer("Blue Spore Bomb", 97)

    def sticky_fungus_energy_fungus(self):
        print("Boss used Sticky Fungus & Energy Fungus!")
        self.set_ability_timer("Sticky Fungus & Energy Fungus", 143)


if __name__ == "__main__":
    croesus_helper = CroesusHelper()

    # Simulate the start of a boss encounter
    croesus_helper.update()

    # Run for a while to allow the timers to trigger
    import time

    time.sleep(30)

    # Stop the timers
    croesus_helper.stop()
