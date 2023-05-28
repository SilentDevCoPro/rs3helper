from rs3helper.plugins.plugin import Plugin
from threading import Timer, Event, Thread
import time


class CroesusHelper(Plugin):
    """Helper class for Croesus boss encounter in a game.

    This class provides warnings for the boss's abilities based on a predefined sequence and time intervals.
    The sequence can be offset to provide warnings earlier or later.

    :param offset: offset time in seconds to shift the warnings earlier or later. Positive values make the warnings
                   earlier, negative values make them later. Default is 0, which means no offset.
    """
    abilities = ["Red Spore Bomb", "Fairy Ring", "Slime Mould", "Yellow Spore Bomb",
                 "Hard Fungus Fall (Stun)", "Sticky Fungus", "Green Spore Bomb", "Blue Spore Bomb",
                 "Sticky Fungus & Energy Fungus"]
    intervals = [14, 9, 15, 13, 12, 9, 14, 11, 14, 12, 11, 9]  # time intervals in seconds

    def __init__(self, offset=0):
        super().__init__("Croesus Helper")
        self.is_boss_encounter_tracking = False
        self.ability_timers = {ability: None for ability in self.abilities}
        self.offset = offset
        self.next_ability_index = 0
        self.countdown_stop_event = Event()
        self.countdown_thread = None

    def update(self):
        """Starts tracking the boss encounter if it's detected and not already being tracked."""
        if self.detect_boss_encounter() and not self.is_boss_encounter_tracking:
            self.start_timers()
            self.is_boss_encounter_tracking = True

    def detect_boss_encounter(self):
        """Detects the boss encounter.

        Currently returns True by default. This should be replaced with actual detection logic.
        """
        return True

    def start_timers(self):
        """
        Starts the timer for the next ability in the rotation.
        """
        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()  # stop the countdown
        self.countdown_thread = None  # reset the thread
        self.countdown_stop_event.clear()  # reset the stop event
        self.print_next_ability()  # print the next ability
        self.start_incoming_attack_timer()  # start the countdown to the next attack
        self.set_ability_timer(self.next_ability_index)
        self.next_ability_index = (self.next_ability_index + 1) % len(self.abilities)

    def set_ability_timer(self, index):
        """Sets a timer for a specific ability.

        When the timer expires, the corresponding method for the ability will be called, and a new timer will be started
        for the next ability in the sequence.

        :param index: index of the ability in the abilities list
        """
        ability = self.abilities[index]
        method_name = ability.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('&', 'and')
        interval = self.intervals[index] - self.offset
        try:
            self.ability_timers[ability] = Timer(max(0, interval), getattr(self, method_name))
            self.ability_timers[ability].start()
        except AttributeError:
            print(f"Method {method_name} does not exist")

    def print_next_ability(self):
        """Prints the name of the next ability that will be triggered."""
        next_ability = self.abilities[self.next_ability_index]
        print(f"Next ability: {next_ability}")

    def start_incoming_attack_timer(self):
        """Starts a timer that counts down to the next attack and prints a warning message when the attack is about to happen."""
        interval = self.intervals[self.next_ability_index] - self.offset
        self.countdown_stop_event.set()  # Stop any existing countdown
        self.countdown_stop_event.clear()  # Prepare for a new countdown
        self.countdown_thread = Thread(target=self.countdown, args=(interval,))
        self.countdown_thread.start()

    def countdown(self, seconds_remaining):
        """Counts down from the given number of seconds, printing a message each second."""
        for i in range(seconds_remaining, 0, -1):
            if self.countdown_stop_event.is_set():
                return  # stop the countdown
            print(f"Incoming attack in {i}")
            time.sleep(1)

    def stop(self):
        """Stops tracking the boss encounter and cancels all timers."""
        self.is_boss_encounter_tracking = False
        for timer in self.ability_timers.values():
            if timer is not None:
                timer.cancel()
        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()

            # define methods for each ability
    # each method prints a warning for the ability and starts a timer for the next ability
    def red_spore_bomb(self):
        print("Boss used Red Spore Bomb!")
        self.start_timers()

    def fairy_ring(self):
        print("Boss used Fairy Ring!")
        self.start_timers()

    def slime_mould(self):
        print("Boss used Slime Mould!")
        self.start_timers()

    def yellow_spore_bomb(self):
        print("Boss used Yellow Spore Bomb!")
        self.start_timers()

    def hard_fungus_fall_stun(self):
        print("Boss used Hard Fungus Fall (Stun)!")
        self.start_timers()

    def sticky_fungus(self):
        print("Boss used Sticky Fungus!")
        self.start_timers()

    def green_spore_bomb(self):
        print("Boss used Green Spore Bomb!")
        self.start_timers()

    def blue_spore_bomb(self):
        print("Boss used Blue Spore Bomb!")
        self.start_timers()

    def sticky_fungus_and_energy_fungus(self):
        print("Boss used Sticky Fungus & Energy Fungus!")
        self.start_timers()


if __name__ == "__main__":
    croesus_helper = CroesusHelper()
    croesus_helper.update()

    time.sleep(120)
