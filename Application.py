import argparse

from utils import isRunningLinux, Log, isUserAdmin, getLinuxVersion
from utils.colors import OutputColors as Colors
from values.Constants import REPO_URL, FILE_PATH, FILENAME, COMPILER_FILENAME
from exceptions import LinuxSystemNotFound, RootPrivilegesNotGiven
from net.PageInfo import Connection
from net.Downloader import Downloader
from net.DependenciesInstaller import Dependencies
from data_manager import UnZipper, Compiler


__program_name = """Kernel Upgrader for Linux"""
__program_description = """Download, compile and install the latest stable kernel for your Linux system. Automate
 this tool for upgrading your kernel periodically"""
__program_version = "Current running version: 0.9d - " + REPO_URL


def main(arg):
    usage = arg.usage
    if usage:
        # __log.d("Showing usage")
        print(Colors.HEADER + __program_name + Colors.ENDC + "\nUse this tool for upgrading your Linux kernel " +
              Colors.UNDERLINE + "automatically" + Colors.ENDC + " with no user interaction. For this purpose," +
              " the tool needs " + Colors.OKGREEN + "admin rights" + Colors.ENDC + " in order to install required" +
              " dependencies and the kernel when everything has finished.\nYou can find " + Colors.BOLD + "the" +
              " program logs" + Colors.ENDC + " at the following location: " + Colors.OKBLUE +
              "\n\t - " + FILE_PATH + FILENAME + Colors.ENDC + ": all program logs\n\t - " + Colors.OKBLUE +
              FILE_PATH + COMPILER_FILENAME + Colors.ENDC + ": kernel compiler logs\n\nYou can find more information" +
              " about this program at the following URL: " + Colors.UNDERLINE + REPO_URL + Colors.ENDC)
        # __log.finish()
    else:
        if not isUserAdmin():
            # __log.e("Running without root privileges")
            # __log.finish()
            raise RootPrivilegesNotGiven("This application needs root rights in order to work properly. Run with"
                                         " \"-u\" option to get more information")
        else:
            __log = Log.instance()
            if not isRunningLinux():
                __log.e("OS is not under a Linux installation. Aborting kernel upgrade...")
                __log.finish()
                raise LinuxSystemNotFound(
                    "Your OS is not running under a Linux installation. It is not possible to update"
                    " the kernel")
            else:
                __log.i("Starting kernel compiling")
                __log.d("Checking versions")
                current_version = getLinuxVersion()
                info = Connection()
                new_version = info.getLatestVersionCode()
                from packaging import version
                if version.parse(current_version) >= version.parse(new_version):
                    __log.d("The version installed is the same or greater than the available one. Current version: " +
                            current_version + " | Available version: " + new_version)
                    print(Colors.WARNING + "You already have the latest version" + Colors.ENDC)
                    exit(1)
                else:
                    print(Colors.OKBLUE + "Downloading new version... " + Colors.ENDC + "| New version: " + new_version)
                    __log.d("Starting new version download... | New version: " + new_version)
                    version_url = info.getLatestVersionURL()
                    downloader = Downloader(version_url, new_version)
                    download_path, current_date = downloader.startDownload()
                    __log.d("Starting dependencies installation...")
                    print(Colors.OKBLUE + "Installing required dependencies... " + Colors.ENDC)
                    Dependencies.installRequiredDependencies()
                    __log.d("Starting kernel decompression")
                    print(Colors.OKBLUE + "Decompressing downloaded kernel..." + Colors.ENDC)
                    unzipper = UnZipper(download_path)
                    kernel_folder = unzipper.unzip()
                    __log.d("Finished kernel decompression")
                    __log.d("Starting kernel compilation...")
                    print(Colors.OKBLUE + "Copying old configuration..." + Colors.ENDC)
                    compiler = Compiler(kernel_folder, new_version, current_date)
                    __log.d("Copying old kernel boot config")
                    if compiler.copy_latest_config():
                        __log.d("Adapting latest config for the new kernel version")
                        print(Colors.OKBLUE + "Adapting old configuration to the new kernel..." + Colors.ENDC)
                        compiler.adaptOldConfig()
                        __log.d("Performing kernel compilation...")
                        print(Colors.OKBLUE + "Starting kernel compilation..." + Colors.ENDC)
                        print(Colors.WARNING + "This process will take a long time to finish. You can do it "
                                               "in background by pressing \"Ctrl + Z\" and then, type \"bg\" at your"
                                               " terminal" + Colors.ENDC)
                        compiler.compileKernel()
                        __log.d("Kernel compilation finished")
                        __log.d("Starting kernel installation...")
                        print(Colors.OKBLUE + "Installing the new kernel..." + Colors.ENDC)
                        compiler.installKernel()
                        __log.d("Finished correctly kernel installation. New version installed: " + new_version)
                        __log.finish()
                        print(Colors.OKGREEN + "Kernel completely installed. Now you should reboot in order to apply"
                                               " changes. New version: " + new_version + Colors.ENDC)
                        exit(0)


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
