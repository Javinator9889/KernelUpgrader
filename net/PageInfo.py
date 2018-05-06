from values.Constants import KERNEL_PAGE, PARSER, LATEST_LINK_ID
from exceptions import raiserModuleNotFound
from utils import Log
# from Application import log


class Connection:
    def __init__(self):
        try:
            from bs4 import BeautifulSoup
            import lxml
            import requests
            saved_page_content = requests.get(KERNEL_PAGE).content
            self.__soupObject = BeautifulSoup(saved_page_content, PARSER)
        except ModuleNotFoundError as e:
            Log.instance().e("Modules not found. " + str(e))
            Log.instance().finish()
            raiserModuleNotFound(e)

    def getLatestVersionCode(self):
        html_latest_version = self.__soupObject.find(id=LATEST_LINK_ID)
        return html_latest_version.title.string

    def getLatestVersionURL(self):
        html_latest_link = self.__soupObject.find(id=LATEST_LINK_ID)
        return html_latest_link.get('href')
