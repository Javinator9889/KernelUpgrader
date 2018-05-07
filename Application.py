import argparse
import time

from utils import isRunningLinux, Log, isUserAdmin, getLinuxVersion, getFreeSpaceAvailable
from utils.colors import OutputColors as Colors
from utils.anim import Animation
from values.Constants import REPO_URL, FILE_PATH, FILENAME, COMPILER_FILENAME
from exceptions import LinuxSystemNotFound, RootPrivilegesNotGiven, raiserModuleNotFound, NotEnoughFreeSpaceAvailable
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
        print(Colors.HEADER + __program_name + Colors.ENDC + "\nUse this tool for upgrading your Linux kernel " +
              Colors.UNDERLINE + "automatically" + Colors.ENDC + " with no user interaction. For this purpose," +
              " the tool needs " + Colors.OKGREEN + "admin rights" + Colors.ENDC + " in order to install required" +
              " dependencies and the kernel when everything has finished.\nYou can find " + Colors.BOLD + "the" +
              " program logs" + Colors.ENDC + " at the following location: " + Colors.OKBLUE +
              "\n\t - " + FILE_PATH + FILENAME + Colors.ENDC + ": all program logs\n\t - " + Colors.OKBLUE +
              FILE_PATH + COMPILER_FILENAME + Colors.ENDC + ": kernel compiler logs\n\nYou can find more information" +
              " about this program at the following URL: " + Colors.UNDERLINE + REPO_URL + Colors.ENDC)
    else:
        if not isUserAdmin():
            raise RootPrivilegesNotGiven("This application needs root rights in order to work properly. Run with"
                                         " \"-u\" option to get more information")
        else:
            __log = Log.instance()
            animator = Animation(0.1)
            try:
                if not isRunningLinux():
                    __log.e("OS is not under a Linux installation. Aborting kernel upgrade...")
                    __log.finish()
                    raise LinuxSystemNotFound(
                        "Your OS is not running under a Linux installation. It is not possible to update"
                        " the kernel")
                else:
                    __log.i("Checking for free space available...")
                    free_space = float(getFreeSpaceAvailable())
                    if free_space < 20:
                        __log.e("There is not enough free space available. Current free space (in GB): "
                                + str(free_space))
                        __log.finish()
                        raise NotEnoughFreeSpaceAvailable("There is not enough free space available on drive which "
                                                          "mounts \"/home\"  20GB are needed at least")
                    __log.i("There is enough free space available. Current free space: " + str(free_space) + " GB")
                    __log.i("Starting kernel compiling")
                    __log.d("Checking versions")
                    current_version = getLinuxVersion()
                    __log.i("Current version detected: " + current_version)
                    info = Connection()
                    new_version = info.getLatestVersionCode()
                    from packaging import version
                    if version.parse(current_version) >= version.parse(new_version):
                        __log.d("The version installed is the same or greater than the available one. "
                                "Current version: " + current_version + " | Available version: " + new_version)
                        print(Colors.FAIL + "You already have the latest version" + Colors.ENDC)
                        exit(1)
                    else:
                        __log.d("There is a new version available - new kernel upgrade process started")
                        print(Colors.OKGREEN + "There is a new version available." +
                              Colors.ENDC)
                        print(Colors.OKBLUE + "Downloading new version... " + Colors.ENDC + "| New version: " +
                              new_version)
                        __log.d("Starting new version download... | New version: " + new_version)
                        version_url = info.getLatestVersionURL()
                        __log.i("Downloading from: " + version_url)
                        downloader = Downloader(version_url, new_version)
                        download_path, current_date = downloader.startDownload()
                        __log.i("Downloaded to path: \"" + download_path + "\"")
                        __log.d("Starting dependencies installation...")
                        print(Colors.OKBLUE + "Installing required dependencies... " + Colors.ENDC)
                        Dependencies.installRequiredDependencies()
                        __log.d("Required dependencies installed/satisfied")
                        __log.d("Starting kernel decompression")
                        animator.animate(Colors.OKBLUE + "Decompressing downloaded kernel..." + Colors.ENDC,
                                         Colors.OKBLUE)
                        unzipper = UnZipper(download_path)
                        kernel_folder = unzipper.unzip()
                        animator.stop()
                        __log.d("Finished kernel decompression")
                        time.sleep(1)
                        __log.d("Starting kernel compilation...")
                        print(Colors.OKBLUE + "Copying old configuration..." + Colors.ENDC)
                        compiler = Compiler(kernel_folder, new_version, current_date)
                        __log.d("Copying old kernel boot config")
                        if compiler.copy_latest_config():
                            __log.d("Copied old kernel boot configuration")
                            __log.d("Adapting latest config for the new kernel version")
                            animator.animate(Colors.OKBLUE + "Adapting old configuration to the new kernel..."
                                             + Colors.ENDC, Colors.OKBLUE)
                            compiler.adaptOldConfig()
                            animator.stop()
                            __log.d("Adapted old kernel configuration to the newer version")
                            time.sleep(1)
                            __log.d("Performing kernel compilation...")
                            print(Colors.OKBLUE + "Starting kernel compilation..." + Colors.ENDC)
                            print(Colors.WARNING + "This process will take a long time to finish. You can do it "
                                                   "in background by pressing \"Ctrl + Z\" and then, type \"bg\" at"
                                                   " your terminal. To resume, just type \"fg\"." + Colors.ENDC)
                            animator.animate(Colors.BOLD + "Performing kernel compilation..." + Colors.ENDC,
                                             Colors.BOLD)
                            compiler.compileKernel()
                            animator.stop()
                            __log.d("Kernel compilation finished")
                            time.sleep(1)
                            __log.d("Starting kernel installation...")
                            animator.animate(Colors.OKBLUE + "Installing the new kernel..." + Colors.ENDC,
                                             Colors.OKBLUE)
                            compiler.installKernel()
                            animator.stop()
                            __log.d("Finished correctly kernel installation. New version installed: " + new_version)
                            time.sleep(1)
                            __log.finish()
                            print(Colors.OKGREEN + "Kernel completely installed. Now you should reboot in order to "
                                                   "apply changes. New version: " + new_version + Colors.ENDC)
                            exit(0)
                        else:
                            __log.e("Impossible to copy latest kernel configuration. Aborting...")
                            __log.finish()
            except ImportError as e:
                raiserModuleNotFound(e)
            except KeyboardInterrupt:
                animator.stop()
                print("\n")
                print(Colors.FAIL + "User pressed Ctrl + C - stopping..." + Colors.ENDC)
                __log.e("User pressed keyboard interrupt. Stopping program...")
                __log.finish()
                exit(2)


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
