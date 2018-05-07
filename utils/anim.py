class Animation:
    __animation_values = "|/-\\"

    def __init__(self, duration):
        self.__duration = duration
        self.__continueAnimation = True

    def animate(self, text):
        from threading import Thread

        if self.__continueAnimation is False:
            self.__continueAnimation = True
        animation_thread = Thread(target=self.__animation, args=(text,))
        animation_thread.start()

    def __animation(self, text):
        import time

        idx = 0
        while self.__continueAnimation:
            print(text + " " + self.__animation_values[idx % len(self.__animation_values)], end="\r")
            idx += 1
            time.sleep(self.__duration)

    def stop(self):
        self.__continueAnimation = False
