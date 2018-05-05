import os
import subprocess

from app.exceptions import ExtractionError, CopyConfigError, OldConfigAdaptationError
from app.utils import getLinuxVersion, getHomeDir, returnToHomeDir


class UnZipper:
    def __init__(self, filename):
        returnToHomeDir()
        self.filename = filename
        self.dir = os.path.dirname(filename)
        file_tar, file_tar_ext = os.path.splitext(filename)
        self.file_unzip, file_unzip_ext = os.path.splitext(file_tar)

    def unzip(self):
        returnToHomeDir()
        import tarfile
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
        self.kernel_folder = kernel_folder
        self.new_kernel_version = new_kernel_version
        self.date = date

    def copy_latest_config(self):
        returnToHomeDir()
        from fnmatch import fnmatch
        kernel_version = getLinuxVersion()
        configs = os.listdir("/boot/")
        pattern = "config-*"
        files_found = []
        for entry in configs:
            if fnmatch(entry, pattern):
                files_found.append(entry)
        if any(substring in files_found for substring in kernel_version):
            from app.values.Constants import COPY_BOOT_CONFIG

            download_path = "{}/Downloads/linux_{}_{}/{}".format(getHomeDir(),
                                                                 self.new_kernel_version,
                                                                 self.date,
                                                                 self.kernel_folder)
            command = COPY_BOOT_CONFIG.format(kernel_version, download_path)
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
        returnToHomeDir()
        from app.values.Constants import ADAPT_OLD_CONFIG
        kernel_path = "{}/Downloads/linux_{}_{}/{}".format(getHomeDir(),
                                                           self.new_kernel_version,
                                                           self.date,
                                                           self.kernel_folder)
        command = ADAPT_OLD_CONFIG.format(kernel_path)
        terminal_process = subprocess.run(command.split(), stderr=subprocess.PIPE)
        if terminal_process.returncode != 0:
            raise OldConfigAdaptationError("There was a problem while trying to update the old configuration for the"
                                           " new kernel. Please, go to kernel dir and run \"make menuconfig\" for"
                                           " updating manually. Error output: "
                                           + terminal_process.stderr.decode("utf'8"))

