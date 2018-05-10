import os
import subprocess
import logging

from kernel_upgrader.exceptions import (
    ExtractionError,
    CopyConfigError,
    OldConfigAdaptationError,
    CompilationError,
    RPMNotSupported,
    InstallationError
)
from kernel_upgrader.utils import *
from kernel_upgrader.values.Constants import LOG_KERNEL, LOG_COMPILER


class UnZipper:
    def __init__(self, filename):
        returnToHomeDir()
        self.__filename = filename
        self.__dir = os.path.dirname(filename)
        file_tar, file_tar_ext = os.path.splitext(filename)
        self.__file_unzip, file_unzip_ext = os.path.splitext(file_tar)
        self.__log = logging.getLogger(LOG_KERNEL)

    def unzip(self):
        # type: () -> str
        import tarfile
        import os.path as path

        returnToHomeDir()
        opened_tar_file = tarfile.open(self.__filename, "r:*")
        opened_tar_file.extractall(path=self.__dir)
        opened_tar_file.close()
        if os.path.exists(self.__file_unzip) and os.path.isdir(self.__file_unzip):
            return path.basename(path.normpath(self.__file_unzip))
        else:
            self.__log.error("There was an error while decompressing 'tar' file located at: " + self.__filename)
            raise ExtractionError(
                OutputColors.FAIL + "There was a problem while decompressing 'tar' file (file does not "
                                    "exists or is not a dir)" + OutputColors.ENDC)


class Compiler:
    def __init__(self, kernel_folder, new_kernel_version, current_date):
        returnToHomeDir()
        home_dir = getHomeDir()
        self.__kernel_path = "{}/linux_{}_{}/{}".format(home_dir,
                                                        new_kernel_version,
                                                        current_date,
                                                        kernel_folder)
        self.__decompressed_path = "{}/linux_{}_{}/".format(home_dir,
                                                            new_kernel_version,
                                                            current_date)
        self.__log = logging.getLogger(LOG_KERNEL)
        self.__log.debug("Kernel path: \"" + self.__kernel_path + "\"")
        self.__log.debug("Decompressed kernel path: \"" + self.__decompressed_path + "\"")
        self.__log.debug(
            "Removing old kernels in order to have enough space available on /root. We will only keep actually"
            " installed version and the new one")
        removeOldKernels()

    def copy_latest_config(self):
        from fnmatch import fnmatch

        returnToHomeDir()
        kernel_version = getLinuxVersion()
        configs = os.listdir("/boot/")
        pattern = "config-*"
        files_found = []
        for entry in configs:
            if fnmatch(entry, pattern):
                files_found.append(entry)
        self.__log.debug("Files found: " + str(files_found))
        any_found = next((config for config in files_found if kernel_version.rstrip() in config), None)
        if any_found is not None:
            from kernel_upgrader.values.Constants import COMPILE_COPY_BOOT_CONFIG

            self.__log.debug("Found old boot config - copying to: \"" + self.__kernel_path + "\"")
            command = COMPILE_COPY_BOOT_CONFIG.format(kernel_version, self.__kernel_path)
            terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if terminal_process.returncode != 0:
                self.__log.error(
                    "An error occurred while copying latest kernel. Error output: " + terminal_process.stderr
                    .decode("utf-8"))
                raise CopyConfigError(OutputColors.FAIL + "No configuration was found or an error occurred while "
                                                          "copying latest kernel boot configuration. Error output: "
                                      + terminal_process.stderr.decode("utf-8") + OutputColors.ENDC)
            else:
                self.__log.debug("Correctly copied old boot config | STDOUT log: "
                                 + terminal_process.stdout.decode("utf-8"))
                return True
        else:
            self.__log.error("No boot configuration found for the current kernel version")
            raise CopyConfigError(OutputColors.FAIL + "No boot configuration was found for the current kernel version."
                                                      " Searching a config for version \"" + kernel_version.rstrip() +
                                  "\" for these files in \"/boot/\" partition\n" + str(files_found) + OutputColors.ENDC)

    def adaptOldConfig(self):
        from kernel_upgrader.values.Constants import COMPILE_ADAPT_OLD_CONFIG

        returnToHomeDir()
        self.__log.debug("Adapting old config copied in folder \"" + self.__kernel_path + "\"")
        terminal_process = subprocess.run(COMPILE_ADAPT_OLD_CONFIG.split(), stderr=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          cwd=self.__kernel_path)
        if terminal_process.returncode != 0:
            self.__log.error("It was impossible to update the old config. Error output: " + terminal_process.stderr
                             .decode("utf-8"))
            raise OldConfigAdaptationError(OutputColors.FAIL + "There was a problem while trying to update the old "
                                                               "configuration for the new kernel. Please, go to kernel "
                                                               "dir and run \"make menuconfig\" for"
                                                               " updating manually. Error output: "
                                           + terminal_process.stderr.decode("utf'8") + OutputColors.ENDC)
        else:
            self.__log.debug("Correctly adapted old kernel configuration | STDOUT log: "
                             + terminal_process.stdout.decode("utf-8"))

    def compileKernel(self):
        from kernel_upgrader.values.Constants import COMPILE_COMPILE_NEW_KERNEL, OP_REPO_URL

        returnToHomeDir()
        self.__log.debug("Starting kernel compilation - log available on \"kernel_upgrader.compiler.log\"")
        number_of_cores = getCPUCount()
        if isDEBSystem():
            command = COMPILE_COMPILE_NEW_KERNEL.format(number_of_cores)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       cwd=self.__kernel_path)
            compiler_log = logging.getLogger(LOG_COMPILER)
            compiler_log.debug("Compiling kernel with " + str(number_of_cores) + " cores")
            compiler_log.debug("Compiling kernel available in folder: \"" + self.__kernel_path + "\"")
            return_code = process.poll()
            while return_code is None:
                current_output = process.stdout.readline()
                if current_output:
                    compiler_log.debug(current_output.strip().decode("utf-8"))
                return_code = process.poll()
            if return_code != 0:
                err = process.stderr.read().decode("utf-8")
                self.__log.error("There was an error while compiling the new kernel. Error output: " + err)
                raise CompilationError(OutputColors.FAIL + "There was an error while compiling the new kernel. "
                                                           "Error output: " + err + OutputColors.ENDC)
            else:
                compiler_log.debug("Correctly compiled kernel")
                self.__log.debug("Correctly compiled log")
        else:
            self.__log.error("RPM systems are not supported by this tool")
            raise RPMNotSupported(OutputColors.FAIL + "RPM systems are not supported by this tool right now: it works"
                                                      " only on DEB ones.\nMaybe doing an upgrade of this program solve"
                                                      " this problem (if RPM kernel upgrade is included in the new"
                                                      " upgrade. Check it on: \"" + OP_REPO_URL + "\")"
                                  + OutputColors.ENDC)

    def installKernel(self):
        from glob import glob
        from kernel_upgrader.values.Constants import COMPILE_INSTALL_NEW_KERNEL, COMPILE_DEB_PKG

        returnToHomeDir()
        self.__log.debug("Starting kernel installation | Kernel source installation path: " + self.__decompressed_path)
        self.__log.info("Using \"glob\" for applying special chars to command")
        deb_pkg_glob = glob(self.__decompressed_path + COMPILE_DEB_PKG)
        process = subprocess.run(COMPILE_INSTALL_NEW_KERNEL.split() + deb_pkg_glob,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 cwd=self.__decompressed_path)
        if process.returncode != 0:
            self.__log.error("There was an error while installing kernel. Error: " + process.stderr.decode("utf-8"))
            raise InstallationError(OutputColors.FAIL + "There was an error while installing the new kernel module."
                                                        " Do not reboot your computer as errors can happen and make "
                                                        "your PC unbootable. Error output: " +
                                    process.stderr.decode("utf-8") + OutputColors.ENDC)
        else:
            self.__log.debug("Installed new kernel")
