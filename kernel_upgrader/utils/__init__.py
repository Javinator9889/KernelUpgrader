from datetime import datetime
from threading import Thread

from kernel_upgrader.utils.colors import *
from kernel_upgrader.utils.anim import *


def getHomeDir():
    # type: () -> str
    return "/home/kernel_upgrader"


def getLinuxVersion():
    # type: () -> str
    import subprocess
    from kernel_upgrader.values.Constants import C_UNAME

    command_execution = subprocess.run(C_UNAME.split(), stdout=subprocess.PIPE)
    return command_execution.stdout.decode("utf-8")


def getCPUCount():
    # type: () -> int
    from psutil import cpu_count
    return cpu_count()


def returnToHomeDir():
    import os
    os.chdir(getHomeDir())


def isDEBSystem():
    # type: () -> bool
    import subprocess
    from kernel_upgrader.values.Constants import COMPILE_RPM_OR_DEB

    try:
        process = subprocess.Popen(COMPILE_RPM_OR_DEB.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return_code = process.returncode
        if return_code != 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return True


def removeOldKernels():
    import subprocess
    from kernel_upgrader.values.Constants import C_CLEAN_KERNELS

    subprocess.run(C_CLEAN_KERNELS.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def cleanupOldLogs():
    from kernel_upgrader.values.Constants import LOG_FILE_PATH, LOG_FILENAME, LOG_COMPILER_FILENAME, \
        LOG_TARFILE_FILENAME, \
        LOG_TARFILE_COMPILER_FILENAME
    import tarfile
    import os

    kernel_log_filename = LOG_FILE_PATH + LOG_FILENAME
    compiler_log_filename = LOG_FILE_PATH + LOG_COMPILER_FILENAME

    tar_log_filename = LOG_FILE_PATH + LOG_TARFILE_FILENAME
    tar_compiler_log_filename = LOG_FILE_PATH + LOG_TARFILE_COMPILER_FILENAME

    if os.path.exists(kernel_log_filename):
        if os.path.exists(tar_log_filename):
            os.remove(tar_log_filename)
        with tarfile.open(tar_log_filename, "w:gz") as tar:
            tar.add(kernel_log_filename, arcname=os.path.basename(kernel_log_filename))
            tar.close()
            os.remove(kernel_log_filename)
    if os.path.exists(compiler_log_filename):
        if os.path.exists(tar_compiler_log_filename):
            os.remove(tar_compiler_log_filename)
        with tarfile.open(tar_compiler_log_filename, "w:gz") as tar:
            tar.add(compiler_log_filename, arcname=os.path.basename(compiler_log_filename))
            tar.close()
            os.remove(compiler_log_filename)


def isRunningLinux():
    import platform
    return platform.system() == "Linux"


def isUserAdmin():
    import os
    # type: () -> bool
    try:
        return os.getuid() == 0
    except AttributeError:
        return False


def getFreeSpaceAvailable():
    # type: () -> float
    import os
    home_dir = getHomeDir()
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    st = os.statvfs(home_dir)
    return "%.2f" % (st.f_bavail * st.f_frsize / 1024 / 1024 / 1024)


def isRunningInBackground():
    # type: () -> bool
    import os
    import sys

    try:
        if os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
            return False
        else:
            return True
    except OSError:
        return True


def cleanupSpace():
    import logging
    import shutil
    from kernel_upgrader.values.Constants import LOG_KERNEL
    from kernel_upgrader.utils.colors import OutputColors as Colors

    try:
        shutil.rmtree(getHomeDir(), ignore_errors=True)
    except OSError as e:
        log = logging.getLogger(LOG_KERNEL)
        log.error("There was an error while trying to clean data in \"" + getHomeDir() + "\". More info: " + str(e))
        raise RuntimeError(Colors.FAIL + "We were not able to clean data in \"" + getHomeDir() + "\". Please, clean it"
                                                                                                 " up manually.\n"
                                                                                                 "More info available "
                                                                                                 "on logs"
                           + Colors.ENDC)


def exportVersion():
    import pickle
    from kernel_upgrader.values.Constants import OP_VERSION

    filename = "version.json"
    version_dict = {"version": OP_VERSION}
    with open(filename, "wb") as file:
        pickle.dump(version_dict, file, pickle.HIGHEST_PROTOCOL)


def isNewVersionAvailable():
    # type: () -> bool
    import requests
    import pickle
    from kernel_upgrader.values.Constants import OP_VERSION, OP_VERSION_RAW

    response = requests.get(OP_VERSION_RAW)
    version_dict = pickle.loads(response.content)
    return version_dict["version"] != OP_VERSION
