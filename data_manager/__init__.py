import os
import subprocess

from exceptions import ExtractionError, CopyConfigError, OldConfigAdaptationError, CompilationError, \
    RPMNotSupported, InstallationError
from utils import *


class UnZipper:
    def __init__(self, filename):
        returnToHomeDir()
        self.__filename = filename
        self.__dir = os.path.dirname(filename)
        file_tar, file_tar_ext = os.path.splitext(filename)
        self.__file_unzip, file_unzip_ext = os.path.splitext(file_tar)
        self.__log = Log.instance()

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
            self.__log.e("There was an error while decompressing 'tar' file located at: " + self.__filename)
            self.__log.finish()
            raise ExtractionError("There was a problem while decompressing 'tar' file (file does not exists or"
                                  " is not a dir)")


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
        self.__log = Log.instance()
        self.__log.d("Kernel path: \"" + self.__kernel_path + "\"")
        self.__log.d("Decompressed kernel path: \"" + self.__decompressed_path + "\"")
        self.__log.d("Removing old kernels in order to have enough space available on /root. We will only keep actually"
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
        self.__log.d("Files found: " + str(files_found))
        any_found = next((config for config in files_found if kernel_version.rstrip() in config), None)
        if any_found is not None:
            from values.Constants import COPY_BOOT_CONFIG

            self.__log.d("Found old boot config - copying to: \"" + self.__kernel_path + "\"")
            command = COPY_BOOT_CONFIG.format(kernel_version, self.__kernel_path)
            terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if terminal_process.returncode != 0:
                self.__log.e("An error occurred while copying latest kernel. Error output: " + terminal_process.stderr
                             .decode("utf-8"))
                self.__log.finish()
                raise CopyConfigError("No configuration was found or an error occurred while copying latest kernel"
                                      " boot configuration. Error output: " + terminal_process.stderr.decode("utf-8"))
            else:
                self.__log.d("Correctly copied old boot config | STDOUT log: "
                             + terminal_process.stdout.decode("utf-8"))
                return True
        else:
            self.__log.e("No boot configuration found for the current kernel version")
            self.__log.finish()
            raise CopyConfigError("No boot configuration was found for the current kernel version. Searching a "
                                  "config for version \"" + kernel_version.rstrip() + "\" for these files in \"/boot/\""
                                                                                      " partition\n" + str(files_found))

    def adaptOldConfig(self):
        from values.Constants import ADAPT_OLD_CONFIG

        returnToHomeDir()
        self.__log.d("Adapting old config copied in folder \"" + self.__kernel_path + "\"")
        terminal_process = subprocess.run(ADAPT_OLD_CONFIG.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                          cwd=self.__kernel_path)
        if terminal_process.returncode != 0:
            self.__log.e("It was impossible to update the old config. Error output: " + terminal_process.stderr
                         .decode("utf-8"))
            self.__log.finish()
            raise OldConfigAdaptationError("There was a problem while trying to update the old configuration for the"
                                           " new kernel. Please, go to kernel dir and run \"make menuconfig\" for"
                                           " updating manually. Error output: "
                                           + terminal_process.stderr.decode("utf'8"))
        else:
            self.__log.d("Correctly adapted old kernel configuration | STDOUT log: "
                         + terminal_process.stdout.decode("utf-8"))

    def compileKernel(self):
        from values.Constants import COMPILE_NEW_KERNEL, REPO_URL

        returnToHomeDir()
        self.__log.d("Starting kernel compilation - log available on \"kernel_upgrader.compiler.log\"")
        number_of_cores = getCPUCount()
        if isDEBSystem():
            command = COMPILE_NEW_KERNEL.format(number_of_cores)
            process = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                       cwd=self.__kernel_path)
            compiler_log = CompilerLog()
            compiler_log.add("Compiling kernel with " + str(number_of_cores) + " cores")
            compiler_log.add("Compiling kernel available in folder: \"" + self.__kernel_path + "\"")
            for stdout_line in iter(process.stdout.readline, ""):
                compiler_log.add((yield stdout_line))
            process.stdout.close()
            # process.communicate()
            return_code = process.wait()
            # compiler_log.finish()
            if return_code != 0:
                err = process.stderr.read()
                self.__log.e("There was an error while compiling the new kernel. Error output: " + err)
                self.__log.finish()
                raise CompilationError("There was an error while compiling the new kernel. Error output: " +
                                       err)
            else:
                compiler_log.add("Correctly compiled kernel")
                compiler_log.finish()
                self.__log.d("Correctly compiled log")
        else:
            self.__log.e("RPM systems are not supported by this tool")
            self.__log.finish()
            raise RPMNotSupported("RPM systems are not supported by this tool right now: it works only on DEB ones."
                                  "\nMaybe doing an upgrade of this program solve this problem (if RPM kernel upgrade"
                                  " is included in the new upgrade. Check it on: \"" + REPO_URL + "\")")

    def installKernel(self):
        from values.Constants import INSTALL_NEW_KERNEL

        returnToHomeDir()
        self.__log.d("Starting kernel installation | Kernel source installation path: " + self.__decompressed_path)
        process = subprocess.run(INSTALL_NEW_KERNEL.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                 cwd=self.__decompressed_path)
        if process.returncode != 0:
            self.__log.e("There was an error while installing kernel. Error: " + process.stderr.decode("utf-8"))
            self.__log.finish()
            raise InstallationError("There was an error while installing the new kernel module. Do not reboot your "
                                    "computer as errors can happen and make your PC unbootable. Error output: " +
                                    process.stderr.decode("utf-8"))
        else:
            self.__log.d("Installed new kernel")
