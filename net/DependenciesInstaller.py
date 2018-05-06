from utils import Log


class Dependencies:
    def __init__(self):
        self.__log = Log.instance()

    def installRequiredDependencies(self):
        import subprocess
        from values.Constants import DEPENDENCIES
        from exceptions import UnableToInstallDependencies

        process = subprocess.run(DEPENDENCIES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            self.__log().e("Impossible to install dependencies. Error output: " + process.stderr.decode("utf-8"))
            self.__log().finish()
            raise UnableToInstallDependencies("There was a problem while trying to install required dependencies."
                                              " Please, install them manually: " + DEPENDENCIES + "\nError output: " +
                                              process.stderr.decode("utf-8"))
        else:
            self.__log().i("Dependencies installation finished")
