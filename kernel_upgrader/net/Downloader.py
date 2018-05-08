from kernel_upgrader.exceptions import raiserModuleNotFound, raiserContentNotAvailable
from kernel_upgrader.values.Constants import DOWNLOAD_LENGTH
from kernel_upgrader.utils import Log


class Downloader:
    def __init__(self, url, version):
        self.__log = Log.instance()
        try:
            from kernel_upgrader.utils import getHomeDir
            import datetime
            self.__url = url
            self.__version = version
            self.__HOME = getHomeDir()
            self.__date = datetime.date.today().strftime("%d%m%y")
        except ImportError as e:
            self.__log.e("Module needed not found -> " + str(e))
            # self.__log.finish()
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
            self.__log.d("Downloading to: " + download_path)
            with open(download_path, "wb") as download:
                response = requests.get(self.__url, stream=True)
                total_length = response.headers.get(DOWNLOAD_LENGTH)
                if total_length is None:
                    download.close()
                    self.__log.e("The kernel is not available actually for download")
                    raiserContentNotAvailable(response.content)
                else:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                              expected_size=(int(total_length) / 1024) + 1):
                        if chunk:
                            download.write(chunk)
                            download.flush()
                    download.close()
                    length_in_mb = int(total_length) / 1000000
                    self.__log.i("Downloaded " + str(total_length) + " bytes (" + str("%.2f" % length_in_mb) + " MB)")
            return download_path, self.__date
        except ImportError as e:
            raiserModuleNotFound(e)
