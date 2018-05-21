from kernel_upgrader.utils.colors import OutputColors as Colors

# Kernel download parameters
WI_KERNEL_PAGE = "https://www.kernel.org/"
WI_PARSER = "lxml"
WI_ASSIDE_ID = "featured"
WI_TABLE_ID = "latest"
WI_LATEST_LINK_ID = "latest_link"

# Download parameters
WD_DOWNLOAD_LENGTH = "content-length"

# Other commands
C_UNAME = "uname -r"
C_DEPENDENCIES = "apt-get install -y build-essential libncurses5-dev gcc libssl-dev bc flex bison libelf-dev"
C_CLEAN_KERNELS = "dpkg -l 'linux-*' | sed '/^ii/!d;/'\"$(uname -r " \
                  "| sed \"s/\(.*\)-\([^0-9]\+\)/\1/\")\"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' " \
                  "| xargs apt-get -y purge"

# Log params
LOG_KERNEL = "kernel_logging"
LOG_COMPILER = "compiler_logging"
LOG_FILE_PATH = "/var/log/"
LOG_FILENAME = "kernel_upgrader.log"
LOG_COMPILER_FILENAME = "kernel_upgrader.compiler.log"
LOG_TARFILE_FILENAME = "kernel_upgrader.latest.tar.gz"
LOG_TARFILE_COMPILER_FILENAME = "kernel_upgrader.compiler.tar.gz"
LOG_FORMAT_TYPE = "%(asctime)s | [%(levelname)s]: %(message)s"

# Compilation commands
COMPILE_COPY_BOOT_CONFIG = "cp -v /boot/config-{} {}/.config"
COMPILE_ADAPT_OLD_CONFIG = "make olddefconfig"
COMPILE_RPM_OR_DEB = "/usr/bin/rpm -q -f /usr/bin/dpkg"
COMPILE_COMPILE_NEW_KERNEL = "make -j{} deb-pkg"
COMPILE_INSTALL_NEW_KERNEL = "dpkg -i"
COMPILE_DEB_PKG = "linux-*.deb"

# Other params
OP_REPO_URL = "https://goo.gl/ZJ4zP9"
OP_VERSION = "1.18.5"
OP_VERSION_RAW = "https://github.com/Javinator9889/KernelUpgrader/raw/master/version.json"

# Program extended usage
EXU_PROGRAM_NAME = """Kernel Upgrader for Linux"""
EXU_USAGE = Colors.HEADER + EXU_PROGRAM_NAME + Colors.ENDC + "\nUse this tool for upgrading your Linux kernel " + \
            Colors.UNDERLINE + "automatically" + Colors.ENDC + " with no user interaction. For this purpose," + \
            " the tool needs " + Colors.OKGREEN + "admin rights" + Colors.ENDC + " in order to install required" + \
            " dependencies and the kernel when everything has finished.\nYou can find " + Colors.BOLD + "the" + \
            " program logs" + Colors.ENDC + " at the following location: " + Colors.OKBLUE + \
            "\n\t - " + LOG_FILE_PATH + LOG_FILENAME + Colors.ENDC + ": all program logs\n\t - " + Colors.OKBLUE + \
            LOG_FILE_PATH + LOG_COMPILER_FILENAME + Colors.ENDC + \
            ": kernel compiler logs\n\nYou can find more information about this program at the following URL: " + \
            Colors.UNDERLINE + OP_REPO_URL + Colors.ENDC + "\nModules that you will need to install: \n" \
            + Colors.OKBLUE + "\t- pip install beautifulsoup4\n\t- pip install lxml\n\t- pip install requests" \
                              "\n\t- pip install clint\n\t- pip install psutil" + Colors.ENDC + Colors.BOLD + \
            "\n\nIf you find any module required that is not mentioned above, please submit it at the given URL" + \
            Colors.ENDC
