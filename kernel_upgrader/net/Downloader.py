import logging

from kernel_upgrader.exceptions import raiserModuleNotFound, raiserContentNotAvailable
from kernel_upgrader.values.Constants import WD_DOWNLOAD_LENGTH, LOG_KERNEL


class Downloader:
    def __init__(self, url, version):
        self.__log = logging.getLogger(LOG_KERNEL)
        try:
            from kernel_upgrader.utils import getHomeDir
            import datetime
            self.__url = url
            self.__version = version
            self.__HOME = getHomeDir()
            self.__date = datetime.date.today().strftime("%d%m%y")
        except ImportError as e:
            self.__log.error("Module needed not found -> " + str(e))
            raiserModuleNotFound(e)

    def startDownload(self):
        # type: () -> (str, str)
        try:
            from urllib.parse import urlparse
            from clint.textui import progress
            import os
            import requests

            path = urlparse(self.__url).path
            filename = os.path.basename(path)
            partial_path = self.__HOME + "/linux_{}_{}/".format(self.__version, self.__date)
            if not os.path.exists(partial_path):
                os.makedirs(partial_path)
            download_path = partial_path + filename
            self.__log.debug("Downloading to: " + download_path)
            with open(download_path, "wb") as download:
                response = requests.get(self.__url, stream=True)
                total_length = response.headers.get(WD_DOWNLOAD_LENGTH)
                if total_length is None:
                    download.close()
                    self.__log.error("The kernel is not available actually for download")
                    raiserContentNotAvailable(response.content)
                else:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                              expected_size=(int(total_length) / 1024) + 1):
                        if chunk:
                            download.write(chunk)
                            download.flush()
                    download.close()
                    length_in_mb = int(total_length) / 1000000
                    self.__log.info(
                        "Downloaded " + str(total_length) + " bytes (" + str("%.2f" % length_in_mb) + " MB)")
            return download_path, self.__date
        except ImportError as e:
            raiserModuleNotFound(e)
