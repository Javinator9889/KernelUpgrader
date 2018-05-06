from datetime import date
from threading import Thread, enumerate


def getHomeDir():
    # type: () -> str
    from pathlib import Path
    return str(Path.home())


def getLinuxVersion():
    # type: () -> str
    import subprocess
    from values.Constants import UNAME

    command_execution = subprocess.run(UNAME.split(), stdout=subprocess.PIPE)
    return command_execution.stdout.decode("utf-8")


def getCPUCount():
    # type: () -> int
    from psutil import cpu_count
    return cpu_count()


def returnToHomeDir():
    import subprocess
    from values.Constants import GOTO_HOME

    subprocess.run(GOTO_HOME.split())


def isDEBSystem():
    # type: () -> bool
    import subprocess
    from values.Constants import RPM_OR_DEB

    process = subprocess.Popen(RPM_OR_DEB.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()
    return_code = process.returncode
    if return_code != 0:
        return True
    else:
        return False


def removeOldKernels():
    import subprocess
    from values.Constants import CLEAN_KERNELS

    subprocess.run(CLEAN_KERNELS.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def cleanupOldLogs():
    from values.Constants import FILE_PATH, FILENAME, COMPILER_FILENAME, TARFILE_FILENAME, TARFILE_COMPILER_FILENAME
    import tarfile
    import os

    kernel_log_filename = FILE_PATH + FILENAME
    compiler_log_filename = FILE_PATH + COMPILER_FILENAME

    if os.path.exists(kernel_log_filename):
        if os.path.exists(TARFILE_FILENAME):
            os.remove(TARFILE_FILENAME)
        with tarfile.open(TARFILE_FILENAME, "w:gz") as tar:
            tar.add(kernel_log_filename, arcname=os.path.basename(kernel_log_filename))
            tar.close()
            os.remove(kernel_log_filename)
    if os.path.exists(compiler_log_filename):
        if os.path.exists(TARFILE_COMPILER_FILENAME):
            os.remove(TARFILE_COMPILER_FILENAME)
        with tarfile.open(TARFILE_COMPILER_FILENAME, "w:gz") as tar:
            tar.add(compiler_log_filename, arcname=os.path.basename(compiler_log_filename))
            tar.close()
            os.remove(compiler_log_filename)


def isRunningLinux():
    import platform
    return platform.system() != "Linux"


def isUserAdmin():
    import os
    # type: () -> bool
    try:
        return os.getuid() == 0
    except AttributeError:
        return False


class Log:
    def __init__(self):
        from values.Constants import FILE_PATH, FILENAME
        cleanupOldLogs()
        self.fileLog = open(FILE_PATH + FILENAME, "w")

    def d(self, message=None):
        """log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [DEBUG]: ")
        self.fileLog.write(log_date + message)
        self.fileLog.flush()"""
        thread = Thread(target=self.__write, args=("DEBUG", message,))
        thread.start()

    def i(self, message=None):
        """log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [INFO]: ")
        self.fileLog.write(log_date + message)
        self.fileLog.flush()"""
        thread = Thread(target=self.__write, args=("INFO", message,))
        thread.start()

    def e(self, message=None):
        """log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [ERROR]: ")
        self.fileLog.write(log_date + message)
        self.fileLog.flush()"""
        thread = Thread(target=self.__write, args=("ERROR", message,))
        thread.start()

    def w(self, message=None):
        """log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [WARNING]: ")
        self.fileLog.write(log_date + message)
        self.fileLog.flush()"""
        thread = Thread(target=self.__write, args=("WARNING", message,))
        thread.start()

    def __write(self, typo=None, message=None):
        log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [" + typo + "]: ")
        self.fileLog.write(log_date + message + "\n")
        self.fileLog.flush()

    def finish(self):
        current_threads = enumerate()
        if len(current_threads) != 1:
            for active_thread in current_threads:
                try:
                    active_thread.join()
                except RuntimeError:
                    continue
        self.fileLog.close()

    class CompilerLog:
        def __init__(self):
            from values.Constants import FILE_PATH, COMPILER_FILENAME
            cleanupOldLogs()
            self.fileLog = open(FILE_PATH + COMPILER_FILENAME, "w")

        def add(self, message):
            thread = Thread(target=self.__write, args=(message,))
            thread.start()

        def __write(self, message):
            log_date = date.today().strftime("%H:%M:%S@%d/%m/%Y [COMPILER]: ")
            self.fileLog.write(log_date + message + "\n")
            self.fileLog.flush()

        def finish(self):
            current_threads = enumerate()
            if len(current_threads) != 1:
                for active_thread in current_threads:
                    try:
                        active_thread.join()
                    except RuntimeError:
                        continue
            self.fileLog.close()
