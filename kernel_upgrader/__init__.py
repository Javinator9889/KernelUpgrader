import argparse
import logging
import time
import traceback

from .data_manager import UnZipper, Compiler
from .exceptions import (LinuxSystemNotFound,
                         RootPrivilegesNotGiven,
                         raiserModuleNotFound,
                         NotEnoughFreeSpaceAvailable
                         )
from .net.DependenciesInstaller import Dependencies
from .net.Downloader import Downloader
from .net.KernelVersions import KernelVersions
from .net.PageInfo import Connection
from .utils import (isRunningLinux,
                    isUserAdmin,
                    getLinuxVersion,
                    getFreeSpaceAvailable,
                    cleanupSpace,
                    isNewVersionAvailable,
                    cleanupOldLogs
                    )
from .utils.anim import Animation
from .utils.colors import OutputColors as Colors
from .utils.logger import setup_logging
from .values.Constants import OP_REPO_URL, EXU_USAGE, OP_VERSION, LOG_FILE_PATH, LOG_FILENAME, LOG_COMPILER_FILENAME

__program_name = """Kernel Upgrader for Linux"""
__program_description = """Download, compile and install the latest stable kernel for your Linux system. Automate
 this tool for upgrading your kernel periodically"""
__program_version = "Current running version: " + OP_VERSION + " - " + OP_REPO_URL


def application(arg):
    usage = arg.usage
    show_version = arg.version
    check_kernel_updates = arg.check
    interactive = arg.interactive
    if usage:
        print(EXU_USAGE)
    elif show_version:
        print(__program_version)
    elif check_kernel_updates:
        if not isRunningLinux():
            raise LinuxSystemNotFound(Colors.FAIL +
                                      "Your OS is not running under a Linux installation. It is not possible"
                                      " to update the kernel" + Colors.ENDC)
        else:
            from packaging import version
            info = Connection()
            current_version = getLinuxVersion()
            new_version = info.getLatestVersionCode()
            if version.parse(current_version) >= version.parse(new_version):
                print(Colors.FAIL + "You already have the latest version: " + current_version + Colors.ENDC)
                exit(1)
            else:
                print(Colors.OKGREEN + "There is a new version available: " + Colors.ENDC + Colors.BOLD + new_version +
                      Colors.ENDC + "\n\nRun this program without \"-c\" (\"--check\") option to upgrade")
                exit(0)
    else:
        if isNewVersionAvailable():
            print(Colors.HEADER + "New version available" + Colors.ENDC + Colors.OKBLUE + " | Download it with pip"
                                                                                          " or go to this URL: "
                  + Colors.ENDC + Colors.UNDERLINE + OP_REPO_URL + Colors.ENDC + "\n")
            time.sleep(8)
        if not isUserAdmin():
            raise RootPrivilegesNotGiven(Colors.FAIL + "This application needs root rights in order to work properly."
                                                       " Run with \"-u\" option to get more information" + Colors.ENDC)
        else:
            cleanupOldLogs()
            setup_logging("kernel_logging", LOG_FILE_PATH + LOG_FILENAME)
            setup_logging("compiler_logging", LOG_FILE_PATH + LOG_COMPILER_FILENAME)
            __log = logging.getLogger("kernel_logging")
            animator = Animation(0.1)
            try:
                if not isRunningLinux():
                    __log.error("OS is not under a Linux installation. Aborting kernel upgrade...")
                    raise LinuxSystemNotFound(Colors.FAIL +
                                              "Your OS is not running under a Linux installation. It is not possible"
                                              " to update the kernel" + Colors.ENDC)
                else:
                    __log.info("Checking for free space available...")
                    free_space = float(getFreeSpaceAvailable())
                    if free_space < 20:
                        __log.error("There is not enough free space available. Current free space (in GB): "
                                    + str(free_space))
                        raise NotEnoughFreeSpaceAvailable(Colors.FAIL + "There is not enough free space available on "
                                                                        "drive which mounts \"/home\"  20GB are needed "
                                                                        "at least" + Colors.ENDC)
                    __log.info("There is enough free space available. Current free space: " + str(free_space) + " GB")
                    __log.info("Starting kernel compiling")
                    __log.debug("Checking versions")
                    current_version = getLinuxVersion()
                    __log.info("Current version detected: " + current_version)
                    from packaging import version
                    if not interactive:
                        info = Connection()
                        new_version = info.getLatestVersionCode()
                        version_url = info.getLatestVersionURL()
                    else:
                        interactive_mode = KernelVersions()
                        available_versions = interactive_mode.obtain_current_available_kernels()
                        __log.info("Available versions:\n" + str(available_versions))
                        supported_versions = []
                        for release in available_versions:
                            release_version = release.get("release_version", None)
                            release_version = release_version.replace("[EOL]", '')
                            if version.parse(current_version) < version.parse(release_version) \
                                    and not version.parse(release_version).is_prerelease:
                                supported_versions.append(release)
                        if len(supported_versions) == 0:
                            __log.debug("The version installed is the same or greater than the available one. "
                                        "Current version: " + current_version)
                            print(Colors.FAIL + "You already have the latest version" + Colors.ENDC)
                            exit(1)
                        __log.info("Supported versions (higher than the current one):\n" + str(supported_versions))
                        i = 0
                        for displayed_version in supported_versions:
                            print(str(i) + ": " + displayed_version.get("release_type") + "\t" +
                                  displayed_version.get("release_version") + "\t\t| Date: " +
                                  displayed_version.get("release_date"))
                            i += 1
                        is_index_correct = False
                        index = -1
                        while not is_index_correct:
                            index = int(input("Number of the version to install: "))
                            if index < len(supported_versions):
                                is_index_correct = True
                        chosen_version = supported_versions[index]
                        new_version = chosen_version["release_version"]
                        version_url = chosen_version["release_url"]
                    if not interactive and version.parse(current_version) >= version.parse(new_version):
                        __log.debug("The version installed is the same or greater than the available one. "
                                    "Current version: " + current_version + " | Available version: " + new_version)
                        print(Colors.FAIL + "You already have the latest version" + Colors.ENDC)
                        exit(1)
                    else:
                        __log.debug("There is a new version available - new kernel upgrade process started")
                        if not interactive:
                            print(Colors.OKGREEN + "There is a new version available." +
                                  Colors.ENDC)
                        print(Colors.OKBLUE + "Downloading new version... " + Colors.ENDC + "| New version: " +
                              new_version)
                        __log.debug("Starting new version download... | New version: " + new_version)
                        __log.info("Downloading from: " + version_url)
                        downloader = Downloader(version_url, new_version)
                        download_path, current_date = downloader.startDownload()
                        __log.info("Downloaded to path: \"" + download_path + "\"")
                        __log.debug("Starting dependencies installation...")
                        print(Colors.OKBLUE + "Installing required dependencies... " + Colors.ENDC)
                        Dependencies.installRequiredDependencies()
                        __log.debug("Required dependencies installed/satisfied")
                        __log.debug("Starting kernel decompression")
                        animator.animate(Colors.OKBLUE + "Decompressing downloaded kernel..." + Colors.ENDC,
                                         Colors.OKBLUE)
                        unzipper = UnZipper(download_path)
                        kernel_folder = unzipper.unzip()
                        animator.stop()
                        __log.debug("Finished kernel decompression")
                        time.sleep(1)
                        __log.debug("Starting kernel compilation...")
                        __log.debug("Cleaning up space of old kernels")
                        print(Colors.OKBLUE + "Copying old configuration & cleaning up space..." + Colors.ENDC)
                        compiler = Compiler(kernel_folder, new_version, current_date)
                        __log.debug("Copying old kernel boot config")
                        if compiler.copy_latest_config():
                            __log.debug("Copied old kernel boot configuration")
                            __log.debug("Adapting latest config for the new kernel version")
                            animator.animate(Colors.OKBLUE + "Adapting old configuration to the new kernel..."
                                             + Colors.ENDC, Colors.OKBLUE)
                            compiler.adaptOldConfig()
                            animator.stop()
                            __log.debug("Adapted old kernel configuration to the newer version")
                            time.sleep(1)
                            __log.debug("Performing kernel compilation...")
                            print(Colors.OKBLUE + "Starting kernel compilation..." + Colors.ENDC)
                            print(Colors.WARNING + "This process will take a long time to finish. You can do it "
                                                   "in background by pressing \"Ctrl + Z\" and then, type \"bg\" at"
                                                   " your terminal. To resume, just type \"fg\"." + Colors.ENDC)
                            animator.animate(Colors.BOLD + "Performing kernel compilation..." + Colors.ENDC,
                                             Colors.BOLD)
                            compiler.compileKernel()
                            animator.stop()
                            __log.debug("Kernel compilation finished")
                            time.sleep(1)
                            __log.debug("Starting kernel installation...")
                            animator.animate(Colors.OKBLUE + "Installing the new kernel..." + Colors.ENDC,
                                             Colors.OKBLUE)
                            compiler.installKernel()
                            animator.stop()
                            __log.debug("Finished correctly kernel installation. New version installed: " + new_version)
                            time.sleep(1)
                            print(Colors.OKGREEN + "Kernel completely installed. Now you should reboot in order to "
                                                   "apply changes. New version: " + new_version + Colors.ENDC)
                            __log.debug("Cleaning-up space for downloaded & compiled files")
                            animator.animate(Colors.UNDERLINE + "Cleaning up used space..." + Colors.ENDC, None)
                            cleanupSpace()
                            animator.stop()
                            __log.debug("Space cleaned-up")
                            time.sleep(1)
                            exit(0)
                        else:
                            __log.error("Impossible to copy latest kernel configuration. Aborting...")
            except ImportError as e:
                raiserModuleNotFound(e)
            except KeyboardInterrupt:
                animator.force_stop()
                print("\n")
                print(Colors.FAIL + "User pressed Ctrl + C - stopping..." + Colors.ENDC)
                __log.error("User pressed keyboard interrupt. Stopping program...")
                exit(2)
            except Exception as e:
                print("Ooops!! There was an unexpected error :O\n\nPlease, refer to: "
                      ">> https://github.com/Javinator9889/KernelUpgrader/issues << and submit the following red code:")
                print(Colors.FAIL)
                print(e)
                traceback.print_exc()
                print(Colors.ENDC)
                animator.force_stop()
                __log.error("Exception catch | " + str(e))
                exit(3)


def main():
    arguments = argparse.ArgumentParser(prog=__program_name,
                                        description=__program_description,
                                        epilog=__program_version)
    arguments.add_argument("-u",
                           "--usage",
                           action="store_true",
                           help="Show full usage of this program")
    arguments.add_argument("-v",
                           "--version",
                           action="store_true",
                           help="Show program version")
    arguments.add_argument("-c",
                           "--check",
                           action="store_true",
                           help="Only checks if there is any new version available")
    arguments.add_argument("-i",
                           "--interactive",
                           action="store_true",
                           help="Launches the KernelUpgrader tool with interactive mode for selecting the kernel "
                                "you want to install")
    args = arguments.parse_args()
    try:
        application(args)
    except Exception as e:
        print(e)
        traceback.print_exc()
        exit(-1)


if __name__ == '__main__':
    main()
