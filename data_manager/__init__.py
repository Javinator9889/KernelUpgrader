import os
import subprocess

from exceptions import ExtractionError, CopyConfigError, OldConfigAdaptationError, CompilationError,\
    RPMNotSupported, InstallationError
from utils import *
from Application import getLog
from utils import Log


class UnZipper:
    def __init__(self, filename):
        returnToHomeDir()
        self.__filename = filename
        self.__dir = os.path.dirname(filename)
        file_tar, file_tar_ext = os.path.splitext(filename)
        self.__file_unzip, file_unzip_ext = os.path.splitext(file_tar)
        self.__log = getLog()

    def unzip(self):
        # type: () -> str
        import tarfile

        returnToHomeDir()
        opened_tar_file = tarfile.open(self.__filename, "r:*")
        opened_tar_file.extractall(path=self.__dir)
        opened_tar_file.close()
        if os.path.exists(self.__file_unzip) and os.path.isdir(self.__file_unzip):
            return self.__file_unzip
        else:
            self.__log.e("There was an error while decompressing 'tar' file located at: " + self.__filename)
            self.__log.finish()
            raise ExtractionError("There was a problem while decompressing 'tar' file (file does not exists or"
                                  " is not a dir)")


class Compiler:
    def __init__(self, kernel_folder, new_kernel_version, current_date):
        returnToHomeDir()
        home_dir = getHomeDir()
        self.__kernel_path = "{}/Downloads/linux_{}_{}/{}".format(home_dir,
                                                                  new_kernel_version,
                                                                  current_date,
                                                                  kernel_folder)
        self.__decompressed_path = "{}/Downloads/linux_{}_{}/".format(home_dir,
                                                                      new_kernel_version,
                                                                      current_date)
        self.__log = getLog()
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
        if any(substring in files_found for substring in kernel_version):
            from values.Constants import COPY_BOOT_CONFIG

            command = COPY_BOOT_CONFIG.format(kernel_version, self.__kernel_path)
            terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE)
            if terminal_process.returncode != 0:
                self.__log.e("An error occurred while copying latest kernel. Error output: " + terminal_process.stderr
                             .decode("utf-8"))
                self.__log.finish()
                raise CopyConfigError("No configuration was found or an error occurred while copying latest kernel"
                                      " boot configuration. Error output: " + terminal_process.stderr.decode("utf-8"))
            else:
                return True
        else:
            self.__log.e("No boot configuration found for the current kernel version")
            self.__log.finish()
            raise CopyConfigError("No boot configuration was found for the current kernel version. Searching a "
                                  "config for version \"" + str(kernel_version) + "\" for these files in \"/boot/\" "
                                                                                  "partition\n" + str(files_found))

    def adaptOldConfig(self):
        from values.Constants import ADAPT_OLD_CONFIG

        returnToHomeDir()
        command = ADAPT_OLD_CONFIG.format(self.__kernel_path)
        terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE)
        if terminal_process.returncode != 0:
            self.__log.e("It was impossible to update the old config. Error output: " + terminal_process.stderr
                         .decode("utf-8"))
            self.__log.finish()
            raise OldConfigAdaptationError("There was a problem while trying to update the old configuration for the"
                                           " new kernel. Please, go to kernel dir and run \"make menuconfig\" for"
                                           " updating manually. Error output: "
                                           + terminal_process.stderr.decode("utf'8"))

    def compileKernel(self):
        from values.Constants import COMPILE_NEW_KERNEL, REPO_URL

        returnToHomeDir()
        number_of_cores = getCPUCount()
        if isDEBSystem():
            command = COMPILE_NEW_KERNEL.format(self.__kernel_path, number_of_cores, "deb-pkg")
            process = subprocess.Popen(command.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            compiler_log = Log.CompilerLog()
            for stdout_line in iter(process.stdout.readline, ""):
                compiler_log.add(stdout_line)
            process.stdout.close()
            return_code = process.wait()
            compiler_log.finish()
            if return_code != 0:
                err = process.stderr.read()
                self.__log.e("There was an error while compiling the new kernel. Error output: " + err)
                self.__log.finish()
                raise CompilationError("There was an error while compiling the new kernel. Error output: " +
                                       err)
        else:
            self.__log.e("RPM systems are not supported by this tool")
            self.__log.finish()
            raise RPMNotSupported("RPM systems are not supported by this tool right now: it works only on DEB ones."
                                  "\nMaybe doing an upgrade of this program solve this problem (if RPM kernel upgrade"
                                  " is included in the new upgrade. Check it on: \"" + REPO_URL + "\")")

    def installKernel(self):
        from values.Constants import INSTALL_NEW_KERNEL

        returnToHomeDir()
        command = INSTALL_NEW_KERNEL.format(self.__decompressed_path)
        process = subprocess.run(command.split(), stderr=subprocess.PIPE)
        if process.returncode != 0:
            self.__log.e("There was an error while installing kernel. Error: " + process.stderr.decode("utf-8"))
            self.__log.finish()
            raise InstallationError("There was an error while installing the new kernel module. Do not reboot your "
                                    "computer as errors can happen and make your PC unbootable. Error output: " +
                                    process.stderr.decode("utf-8"))
