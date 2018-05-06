import os
import subprocess

from app.exceptions import ExtractionError, CopyConfigError, OldConfigAdaptationError, CompilationError,\
    RPMNotSupported, InstallationError
from app.utils import *


class UnZipper:
    def __init__(self, filename):
        returnToHomeDir()
        self.filename = filename
        self.dir = os.path.dirname(filename)
        file_tar, file_tar_ext = os.path.splitext(filename)
        self.file_unzip, file_unzip_ext = os.path.splitext(file_tar)

    def unzip(self):
        import tarfile

        returnToHomeDir()
        opened_tar_file = tarfile.open(self.filename, "r:*")
        opened_tar_file.extractall(path=self.dir)
        opened_tar_file.close()
        if os.path.exists(self.file_unzip) and os.path.isdir(self.file_unzip):
            return self.file_unzip
        else:
            raise ExtractionError("There was a problem while decompressing 'tar' file (file does not exists or"
                                  " is not a dir)")


class Compiler:
    def __init__(self, kernel_folder, new_kernel_version, date):
        returnToHomeDir()
        home_dir = getHomeDir()
        self.kernel_path = "{}/Downloads/linux_{}_{}/{}".format(home_dir,
                                                                new_kernel_version,
                                                                date,
                                                                kernel_folder)
        self.decompressed_path = "{}/Downloads/linux_{}_{}/".format(home_dir,
                                                                    new_kernel_version,
                                                                    date)
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
        if any(substring in files_found for substring in kernel_version):
            from app.values.Constants import COPY_BOOT_CONFIG

            command = COPY_BOOT_CONFIG.format(kernel_version, self.kernel_path)
            terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE)
            if terminal_process.returncode != 0:
                raise CopyConfigError("No configuration was found or an error occurred while copying latest kernel"
                                      " boot configuration. Error output: " + terminal_process.stderr.decode("utf-8"))
            else:
                return True
        else:
            raise CopyConfigError("No boot configuration was found for the current kernel version. Searching a "
                                  "config for version \"" + str(kernel_version) + "\" for these files in \"/boot/\" "
                                                                                  "partition\n" + str(files_found))

    def adaptOldConfig(self):
        from app.values.Constants import ADAPT_OLD_CONFIG

        returnToHomeDir()
        command = ADAPT_OLD_CONFIG.format(self.kernel_path)
        terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE)
        if terminal_process.returncode != 0:
            raise OldConfigAdaptationError("There was a problem while trying to update the old configuration for the"
                                           " new kernel. Please, go to kernel dir and run \"make menuconfig\" for"
                                           " updating manually. Error output: "
                                           + terminal_process.stderr.decode("utf'8"))

    def compileKernel(self):
        from app.values.Constants import COMPILE_NEW_KERNEL, REPO_URL

        returnToHomeDir()
        number_of_cores = getCPUCount()
        if isDEBSystem():
            command = COMPILE_NEW_KERNEL.format(self.kernel_path, number_of_cores, "deb-pkg")
            process = subprocess.run(command.split(), stderr=subprocess.PIPE)
            if process.returncode != 0:
                raise CompilationError("There was an error while compiling the new kernel. Error output: " +
                                       process.stderr.decode("utf-8"))
        else:
            raise RPMNotSupported("RPM systems are not supported by this tool right now: it works only on DEB ones."
                                  "\nMaybe doing an upgrade of this program solve this problem (if RPM kernel upgrade"
                                  " is included in the new upgrade. Check it on: \"" + REPO_URL + "\")")

    def installKernel(self):
        from app.values.Constants import INSTALL_NEW_KERNEL

        returnToHomeDir()
        command = INSTALL_NEW_KERNEL.format(self.decompressed_path)
        process = subprocess.run(command.split(), stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise InstallationError("There was an error while installing the new kernel module. Do not reboot your "
                                    "computer as errors can happen and make your PC unbootable. Error output: " +
                                    process.stderr.decode("utf-8"))
