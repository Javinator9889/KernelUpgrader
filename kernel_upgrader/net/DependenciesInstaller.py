class Dependencies:
    @staticmethod
    def installRequiredDependencies():
        import subprocess
        import logging
        from kernel_upgrader.values.Constants import C_DEPENDENCIES, LOG_KERNEL
        from kernel_upgrader.exceptions import UnableToInstallDependencies
        from kernel_upgrader.utils.colors import OutputColors as Colors

        __log = logging.getLogger(LOG_KERNEL)
        process = subprocess.run(C_DEPENDENCIES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            __log.error("Impossible to install dependencies. Error output: " + process.stderr.decode("utf-8"))
            raise UnableToInstallDependencies(Colors.FAIL + "There was a problem while trying to install required "
                                                            "dependencies. Please, install them manually: "
                                              + C_DEPENDENCIES + "\nError output: " + process.stderr.decode("utf-8") +
                                              Colors.ENDC)
        else:
            __log.info("Dependencies installation finished")
