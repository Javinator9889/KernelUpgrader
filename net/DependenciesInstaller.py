class Dependencies:
    @staticmethod
    def installRequiredDependencies():
        import subprocess
        from values import DEPENDENCIES
        from exceptions import UnableToInstallDependencies
        from Application import getLog
        process = subprocess.run(DEPENDENCIES.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            getLog().e("Impossible to install dependencies. Error output: " + process.stderr.decode("utf-8"))
            getLog().finish()
            raise UnableToInstallDependencies("There was a problem while trying to install required dependencies."
                                              " Please, install them manually: " + DEPENDENCIES + "\nError output: " +
                                              process.stderr.decode("utf-8"))
        else:
            getLog().i("Dependencies installation finished")
