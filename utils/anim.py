from threading import Event


class Animation:
    __animation_values = "|/-\\"

    def __init__(self, duration):
        self.__duration = duration
        self.__stop_event = Event()

    def animate(self, text, color=None):
        from threading import Thread

        self.__stop_event.clear()
        animation_thread = Thread(target=self.__animation, args=(text, color,))
        animation_thread.setDaemon(True)
        animation_thread.start()

    def __animation(self, text, color=None):
        import time
        from utils.colors import OutputColors

        idx = 0
        if color is None:
            end_color = ""
            color = ""
        else:
            end_color = OutputColors.ENDC
        while not self.__stop_event.is_set():
            print(text + " " + color + "[" + self.__animation_values[idx % len(self.__animation_values)] + "]"
                  + end_color, end="\r")
            idx += 1
            time.sleep(self.__duration)
        print("\n")

    def stop(self):
        self.__stop_event.set()
