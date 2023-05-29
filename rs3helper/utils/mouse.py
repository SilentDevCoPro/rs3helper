from pynput.mouse import Listener


class Mouse:
    def __init__(self):
        self.clicks = []

    def on_click(self, x, y, _, pressed):
        if pressed:
            self.clicks.append((x, y))
            print('Mouse clicked at ({0}, {1})'.format(x, y))
            if len(self.clicks) == 2:
                # Stop listener
                self.clicks.sort()
                return False

    def start_listener(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()
