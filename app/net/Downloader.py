from app.exceptions import raiserModuleNotFound, raiserContentNotAvailable
from app.values.Constants import DOWNLOAD_LENGTH


class Downloader:
    def __init__(self, url, version):
        try:
            from pathlib import Path
            import datetime
            self.url = url
            self.version = version
            self.HOME = str(Path.home())
            self.date = datetime.date.today().strftime("%d%m%y")
        except ModuleNotFoundError as e:
            raiserModuleNotFound(e)

    def startDownload(self):
        from urllib.parse import urlparse
        import os
        import sys
        import requests
        path = urlparse(self.url).path
        filename = os.path.basename(path)
        partial_path = "/Downloads/linux_{}_{}/".format(self.version, self.date)
        download_path = self.HOME + partial_path + filename
        with open(download_path, "wb") as download:
            response = requests.get(self.url, stream=True)
            total_length = response.headers.get(DOWNLOAD_LENGTH)
            if total_length is None:
                download.close()
                raiserContentNotAvailable(response.content)
            else:
                bytes_downloaded = 0
                total_length = int(total_length)
                for data_obtained in response.iter_content(chunk_size=4096):
                    bytes_downloaded += len(data_obtained)
                    download.write(data_obtained)
                    completed = int(50 * bytes_downloaded / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * completed, ' ' * (50 - completed)))
                    sys.stdout.flush()
                download.flush()
                download.close()
        return download_path
