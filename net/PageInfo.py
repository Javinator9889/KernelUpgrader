from values.Constants import KERNEL_PAGE, PARSER, LATEST_LINK_ID
from exceptions import raiserModuleNotFound
from Application import getLog


class Connection:
    def __init__(self):
        try:
            from bs4 import BeautifulSoup
            import lxml
            import requests
            saved_page_content = requests.get(KERNEL_PAGE).content
            self.__soupObject = BeautifulSoup(saved_page_content, PARSER)
        except ModuleNotFoundError as e:
            getLog().e("Modules not found. " + str(e))
            getLog().finish()
            raiserModuleNotFound(e)

    def getLatestVersionCode(self):
        html_latest_version = self.__soupObject.find(id=LATEST_LINK_ID)
        return html_latest_version.title.string

    def getLatestVersionURL(self):
        html_latest_link = self.__soupObject.find(id=LATEST_LINK_ID)
        return html_latest_link.get('href')
