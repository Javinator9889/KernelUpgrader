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
DEPENDENCIES = "apt-get install -y build-essential libncurses5-dev gcc libssl-dev bc"
CLEAN_KERNELS = "dpkg -l 'linux-*' | sed '/^ii/!d;/'\"$(uname -r " \
                "| sed \"s/\(.*\)-\([^0-9]\+\)/\1/\")\"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' " \
                "| xargs apt-get -y purge"

# Log params
FILE_PATH = "/var/log/"
FILENAME = "kernel_upgrader.log"
COMPILER_FILENAME = "kernel_upgrader.compiler.log"
TARFILE_FILENAME = "kernel_upgrader.latest.tar.gz"
TARFILE_COMPILER_FILENAME = "kernel_upgrader.compiler.tar.gz"

# Compilation commands
COPY_BOOT_CONFIG = "cp -v /boot/config-{} {}/.config"
ADAPT_OLD_CONFIG = "cd {} && make olddefconfig"
GOTO_HOME = "cd"
RPM_OR_DEB = "/usr/bin/rpm -q -f /usr/bin/dpkg"
COMPILE_NEW_KERNEL = "cd {} && make -j{} {}"
INSTALL_NEW_KERNEL = "cd {} && dpkg -i linux-*.deb"

# Other params
REPO_URL = "https://goo.gl/ZJ4zP9"
