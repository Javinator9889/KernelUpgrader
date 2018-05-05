KERNEL_PAGE = "https://www.kernel.org/"
PARSER = "lxml"
LATEST_LINK_ID = "latest_link"

DOWNLOAD_LENGTH = "content-length"

UNAME = "uname -r"

COPY_BOOT_CONFIG = "cp -v /boot/config-{} {}/.config"
ADAPT_OLD_CONFIG = "cd {} && make olddefconfig"
GOTO_HOME = "cd"
