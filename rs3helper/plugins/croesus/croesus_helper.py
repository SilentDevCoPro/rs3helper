from rs3helper.plugins.plugin import Plugin
from rs3helper.plugins.croesus.croesus_gui import CroesusGUI
from rs3helper.utils.screen_capture import ScreenCapture
from rs3helper.utils.mouse import Mouse
from rs3helper.utils.ocr import OCR
from threading import Timer, Event, Thread
from queue import Queue
from PyQt6.QtWidgets import QApplication
import sys
import time
import re


class CroesusHelper(Plugin):
    """Helper class for Croesus boss encounter in a game.

    This class provides warnings for the boss's abilities based on a predefined sequence and time intervals.
    The sequence can be offset to provide warnings earlier or later.

    :param offset: offset time in seconds to shift the warnings earlier or later. Positive values make the warnings
                   earlier, negative values make them later. Default is 0, which means no offset.
    """
    abilities = ["Red Spore Bomb", "Fairy Ring", "Slime Mould", "Yellow Spore Bomb",
                 "Hard Fungus Fall (Stun)", "Sticky Fungus", "Green Spore Bomb",
                 "Fairy Ring", "Slime Mould", "Blue Spore Bomb",
                 "Hard Fungus Fall (Stun)", "Energy Fungus"]
    intervals = [14, 9, 15, 13, 12, 9, 14, 11, 14, 12, 11, 9]  # time intervals in seconds

    def __init__(self, offset=0):
        super().__init__("Croesus Helper")
        self.queue = Queue()
        self.app = QApplication([])
        self.gui = CroesusGUI(self.queue, self)
        self.gui.show()
        self.is_boss_encounter_tracking = False
        self.ability_timers = {ability: None for ability in self.abilities}
        self.offset = offset
        self.next_ability_index = 0
        self.countdown_stop_event = Event()
        self.countdown_thread = None
        self.screen_capture = ScreenCapture()
        self.mouse = Mouse()
        self.is_boss_encounter_running = False
        self.paused = False

    def update(self):
        """Starts tracking the boss encounter if it's detected and not already being tracked."""
        print("Update function running...")
        self.is_boss_encounter_running = self.detect_boss_encounter()
        print("STATE: " + str(self.is_boss_encounter_running) + str(self.is_boss_encounter_tracking))
        if self.is_boss_encounter_running and not self.is_boss_encounter_tracking:
            print("STARTING TIMERS")
            self.start_timers()
            self.is_boss_encounter_tracking = True
            self.start()

    def detect_boss_encounter(self):
        """Detects the boss encounter."""
        # self.mouse.start_listener()
        # screen_capture = ScreenCapture()
        # cropped_screenshot = screen_capture.get_cropped_screenshot(self.mouse.clicks)
        # text = OCR.extract_text(cropped_screenshot)
        # match = re.search(r"\b\d{2}:\d{2}\b", text)
        # if match:
        #     print("Boss timer found")
        return True
        # print("Boss timer not found.")
        # return False

    def start_timers(self):
        """
        Starts the timer for the next ability in the rotation.
        """
        # Ensure any running countdown thread is terminated before starting a new one
        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()
            self.countdown_thread.join()

        self.countdown_thread = None
        self.countdown_stop_event.clear()
        self.print_next_ability()
        self.start_incoming_attack_timer()
        self.set_ability_timer(self.next_ability_index)
        self.next_ability_index = (self.next_ability_index + 1) % len(self.abilities)

    def pause(self):
        """Pauses tracking the boss encounter and pauses all timers."""
        self.paused = True
        for timer in self.ability_timers.values():
            if timer is not None:
                timer.cancel()
        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()

    def resume(self):
        """Resumes tracking the boss encounter and resumes all timers."""
        self.paused = False
        self.start_timers()

    def reset(self):
        """Resets the boss encounter back to the start."""
        self.next_ability_index = 0

        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()
            # Give time for the thread to properly terminate
            self.countdown_thread.join()

        # Cancel all ability timers
        for timer in self.ability_timers.values():
            if timer is not None:
                timer.cancel()

        # Ensure the stop event is cleared before starting timers again
        self.countdown_stop_event.clear()
        self.start_timers()

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
            self.queue.put(("start_timer", ability))
        except AttributeError:
            print(f"Method {method_name} does not exist")

    def print_next_ability(self):
        """Prints the name of the next ability that will be triggered."""
        next_ability = self.abilities[self.next_ability_index]
        self.queue.put(("ability", next_ability))

    def start_incoming_attack_timer(self):
        """Starts a timer that counts down to the next attack and prints a warning message when the attack is about to happen."""
        interval = self.intervals[self.next_ability_index] - self.offset
        self.countdown_stop_event.set()
        self.countdown_stop_event.clear()
        self.countdown_thread = Thread(target=self.countdown, args=(interval,))
        self.countdown_thread.start()

    def countdown(self, seconds_remaining):
        """Counts down from the given number of seconds, printing a message each second."""
        for i in range(seconds_remaining, 0, -1):
            if self.countdown_stop_event.is_set():
                return
            self.queue.put(("countdown", i))
            time.sleep(1)

    def start(self):
        sys.exit(self.app.exec())

    def stop(self):
        """Stops tracking the boss encounter and cancels all timers."""
        self.is_boss_encounter_tracking = False
        for timer in self.ability_timers.values():
            if timer is not None:
                timer.cancel()
        if self.countdown_thread is not None and self.countdown_thread.is_alive():
            self.countdown_stop_event.set()

    def red_spore_bomb(self):
        print("Boss used Red Spore Bomb!")
        self.start_timers()
        self.queue.put(("flash", None))

    def fairy_ring(self):
        print("Boss used Fairy Ring!")
        self.start_timers()
        self.queue.put(("flash", None))

    def slime_mould(self):
        print("Boss used Slime Mould!")
        self.start_timers()
        self.queue.put(("flash", None))

    def yellow_spore_bomb(self):
        print("Boss used Yellow Spore Bomb!")
        self.start_timers()
        self.queue.put(("flash", None))

    def hard_fungus_fall_stun(self):
        print("Boss used Hard Fungus Fall (Stun)!")
        self.start_timers()
        self.queue.put(("flash", None))

    def sticky_fungus(self):
        print("Boss used Sticky Fungus!")
        self.start_timers()
        self.queue.put(("flash", None))

    def green_spore_bomb(self):
        print("Boss used Green Spore Bomb!")
        self.start_timers()
        self.queue.put(("flash", None))

    def blue_spore_bomb(self):
        print("Boss used Blue Spore Bomb!")
        self.start_timers()
        self.queue.put(("flash", None))

    def sticky_fungus_and_energy_fungus(self):
        print("Boss used Sticky Fungus & Energy Fungus!")
        self.start_timers()
        self.queue.put(("flash", None))
