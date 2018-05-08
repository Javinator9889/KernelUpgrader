class Dependencies:
    @staticmethod
    def installRequiredDependencies():
        import subprocess
        from kernel_upgrader.values.Constants import DEPENDENCIES
        from kernel_upgrader.exceptions import UnableToInstallDependencies
        from kernel_upgrader.utils import Log
        from kernel_upgrader.utils.colors import OutputColors as Colors

        __log = Log.instance()
        process = subprocess.run(DEPENDENCIES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            __log.e("Impossible to install dependencies. Error output: " + process.stderr.decode("utf-8"))
            __log.finish()
            raise UnableToInstallDependencies(Colors.FAIL + "There was a problem while trying to install required "
                                                            "dependencies. Please, install them manually: "
                                              + DEPENDENCIES + "\nError output: " + process.stderr.decode("utf-8") +
                                              Colors.ENDC)
        else:
            __log.i("Dependencies installation finished")
