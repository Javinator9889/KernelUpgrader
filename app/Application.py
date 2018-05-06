import argparse

from app.utils import isRunningLinux, Log
from app.utils.colors import OutputColors as Colors
from app.values.Constants import REPO_URL, FILE_PATH, FILENAME, COMPILER_FILENAME
from app.exceptions import LinuxSystemNotFound


__program_name = """Kernel Upgrader for Linux"""
__program_description = """Download, compile and install the latest stable kernel for your Linux system. Automate
 this tool for upgrading your kernel periodically"""
__program_version = "Current running version: 0.9d - " + REPO_URL
__log = Log()


def main(arg):
    usage = arg.usage
    if usage:
        __log.d("Showing usage")
        print(Colors.HEADER + __program_name + Colors.ENDC + "\nUse this tool for upgrading your Linux kernel" +
              Colors.UNDERLINE + " automatically" + Colors.ENDC + " with no user interaction. For this purpose," +
              " the tool needs " + Colors.OKGREEN + "admin rights" + Colors.ENDC + " in order to install required" +
              " dependencies and the kernel when everything has finished.\nYou can find " + Colors.BOLD + "the" +
              " program logs" + Colors.ENDC + "at the following location: " + Colors.OKBLUE +
              "\n\t - " + FILE_PATH + FILENAME + Colors.ENDC + ": all program logs\n\t - " + Colors.OKBLUE +
              FILE_PATH + COMPILER_FILENAME + Colors.ENDC + ": kernel compiler logs\n\nYou can find more information" +
              " about this program at the following URL: " + Colors.UNDERLINE + REPO_URL + Colors.ENDC)
        __log.finish()
    else:
        if not isRunningLinux():
            __log.e("OS is not under a Linux installation. Aborting kernel upgrade...")
            __log.finish()
            raise LinuxSystemNotFound("Your OS is not running under a Linux installation. It is not possible to update"
                                      " the kernel")


def getLog():
    return __log


if __name__ == '__main__':
    arguments = argparse.ArgumentParser(prog=__program_name,
                                        description=__program_description,
                                        epilog=__program_version)
    arguments.add_argument("-u",
                           "--usage",
                           action="store_true",
                           help="Show full usage of this program")
    args = arguments.parse_args()
    main(args)
