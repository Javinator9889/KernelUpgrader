from kernel_upgrader.utils.colors import OutputColors as Colors

# Kernel download parameters
KERNEL_PAGE = "https://www.kernel.org/"
PARSER = "lxml"
ASSIDE_ID = "featured"
TABLE_ID = "latest"
LATEST_LINK_ID = "latest_link"

# Download parameters
DOWNLOAD_LENGTH = "content-length"

# Other commands
UNAME = "uname -r"
DEPENDENCIES = "apt-get install -y build-essential libncurses5-dev gcc libssl-dev bc flex bison libelf-dev"
CLEAN_KERNELS = "dpkg -l 'linux-*' | sed '/^ii/!d;/'\"$(uname -r " \
                "| sed \"s/\(.*\)-\([^0-9]\+\)/\1/\")\"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' " \
                "| xargs apt-get -y purge"
CLEAN_DOWNLOADS = "rm -r {}"

# Log params
FILE_PATH = "/var/log/"
FILENAME = "kernel_upgrader.log"
COMPILER_FILENAME = "kernel_upgrader.compiler.log"
TARFILE_FILENAME = "kernel_upgrader.latest.tar.gz"
TARFILE_COMPILER_FILENAME = "kernel_upgrader.compiler.tar.gz"

# Compilation commands
COPY_BOOT_CONFIG = "cp -v /boot/config-{} {}/.config"
ADAPT_OLD_CONFIG = "make olddefconfig"
RPM_OR_DEB = "/usr/bin/rpm -q -f /usr/bin/dpkg"
COMPILE_NEW_KERNEL = "make -j{} deb-pkg"
INSTALL_NEW_KERNEL = "dpkg -i linux-*.deb"

# Other params
REPO_URL = "https://goo.gl/ZJ4zP9"
VERSION = "1.17.2"
VERSION_RAW = "https://github.com/Javinator9889/KernelUpgrader/raw/master/version.json"

# Program extended usage
__program_name = """Kernel Upgrader for Linux"""
USAGE = Colors.HEADER + __program_name + Colors.ENDC + "\nUse this tool for upgrading your Linux kernel " + \
        Colors.UNDERLINE + "automatically" + Colors.ENDC + " with no user interaction. For this purpose," + \
        " the tool needs " + Colors.OKGREEN + "admin rights" + Colors.ENDC + " in order to install required" + \
        " dependencies and the kernel when everything has finished.\nYou can find " + Colors.BOLD + "the" + \
        " program logs" + Colors.ENDC + " at the following location: " + Colors.OKBLUE + \
        "\n\t - " + FILE_PATH + FILENAME + Colors.ENDC + ": all program logs\n\t - " + Colors.OKBLUE + \
        FILE_PATH + COMPILER_FILENAME + Colors.ENDC + \
        ": kernel compiler logs\n\nYou can find more information about this program at the following URL: " + \
        Colors.UNDERLINE + REPO_URL + Colors.ENDC + "\nModules that you will need to install: \n" + Colors.OKBLUE + \
        "\t- pip install beautifulsoup4\n\t- pip install lxml\n\t- pip install requests\n\t- pip install clint\n\t" \
        "- pip install psutil" + Colors.ENDC + Colors.BOLD + "\n\nIf you find any module required that is not " \
                                                             "mentioned above, please submit it at the given URL" + \
        Colors.ENDC
