class ModuleNeededNotFound(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ContentNotAvailable(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def raiserModuleNotFound(exception):
    raise ModuleNeededNotFound("This app requires some modules that were not found on this device. More info:"
                               " " + str(exception))


def raiserContentNotAvailable(exception):
    raise ContentNotAvailable("The content is not available to download. Please, try again later or check your Internet"
                              " connection. More info: " + str(exception))
