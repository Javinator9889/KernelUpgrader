class ModuleNeededNotFound(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(ModuleNeededNotFound, self).__init__(message)


class ContentNotAvailable(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(ContentNotAvailable, self).__init__(message)


class ExtractionError(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(ExtractionError, self).__init__(message)


class CopyConfigError(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(CopyConfigError, self).__init__(message)


class OldConfigAdaptationError(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)


class CompilationError(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(CompilationError, self).__init__(message)


class RPMNotSupported(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(RPMNotSupported, self).__init__(message)


class InstallationError(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(InstallationError, self).__init__(message)


class LinuxSystemNotFound(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(LinuxSystemNotFound, self).__init__(message)


class RootPrivilegesNotGiven(RuntimeError):
    def __init__(self, message=None):
        self.message = message
        super(RootPrivilegesNotGiven, self).__init__(message)


class UnableToInstallDependencies(RuntimeError):
    def __init__(self, message):
        self.message = message
        super(UnableToInstallDependencies, self).__init__(message)


class NotEnoughFreeSpaceAvailable(RuntimeError):
    def __init__(self, message):
        self.message = message
        super(NotEnoughFreeSpaceAvailable, self).__init__(message)


def raiserModuleNotFound(exception):
    from kernel_upgrader.utils.colors import OutputColors as Colors
    raise ModuleNeededNotFound(Colors.FAIL + "This app requires some modules that were not found on this device."
                                             " More info: " + str(exception) + Colors.ENDC)


def raiserContentNotAvailable(exception):
    from kernel_upgrader.utils.colors import OutputColors as Colors
    raise ContentNotAvailable(Colors.FAIL + "The content is not available to download. Please, try again later or "
                                            "check your Internet connection. More info: "
                              + str(exception) + Colors.ENDC)
