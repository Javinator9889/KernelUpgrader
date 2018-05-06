from exceptions import raiserModuleNotFound, raiserContentNotAvailable
from values.Constants import DOWNLOAD_LENGTH
from Application import getLog


class Downloader:
    def __init__(self, url, version):
        self.__log = getLog()
        try:
            from utils import getHomeDir
            import datetime
            self.__url = url
            self.__version = version
            self.__HOME = getHomeDir()
            self.__date = datetime.date.today().strftime("%d%m%y")
        except ModuleNotFoundError as e:
            self.__log.e("Module needed not found -> " + str(e))
            self.__log.finish()
            raiserModuleNotFound(e)

    def startDownload(self):
        # type: () -> (str, str)
        from urllib.parse import urlparse
        import os
        import sys
        import requests
        path = urlparse(self.__url).path
        filename = os.path.basename(path)
        partial_path = "/Downloads/linux_{}_{}/".format(self.__version, self.__date)
        download_path = self.__HOME + partial_path + filename
        self.__log.d("Downloading to: " + download_path)
        with open(download_path, "wb") as download:
            response = requests.get(self.__url, stream=True)
            total_length = response.headers.get(DOWNLOAD_LENGTH)
            if total_length is None:
                download.close()
                self.__log.e("The kernel is not available actually for download")
                raiserContentNotAvailable(response.content)
            else:
                bytes_downloaded = 0
                total_length = int(total_length)
                for data_obtained in response.iter_content(chunk_size=4096):
                    bytes_downloaded += len(data_obtained)
                    download.write(data_obtained)
                    completed = int(50 * bytes_downloaded / total_length)
                    sys.stdout.__write("\r[%s%s]" % ('=' * completed, ' ' * (50 - completed)))
                    sys.stdout.flush()
                download.flush()
                download.close()
                length_in_mb = total_length / 1000000
                self.__log.i("Downloaded " + str(total_length) + " bytes (" + str("%.2f" % length_in_mb) + " MB)")
        return download_path, self.__date
