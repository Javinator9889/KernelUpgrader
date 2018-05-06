class Dependencies:
    @staticmethod
    def installRequiredDependencies():
        import subprocess
        from values.Constants import DEPENDENCIES
        from exceptions import UnableToInstallDependencies
        from Application import log
        process = subprocess.run(DEPENDENCIES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            log().e("Impossible to install dependencies. Error output: " + process.stderr.decode("utf-8"))
            log().finish()
            raise UnableToInstallDependencies("There was a problem while trying to install required dependencies."
                                              " Please, install them manually: " + DEPENDENCIES + "\nError output: " +
                                              process.stderr.decode("utf-8"))
        else:
            log().i("Dependencies installation finished")
