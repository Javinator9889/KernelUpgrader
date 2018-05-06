from values.Constants import KERNEL_PAGE, PARSER, ASSIDE_ID, TABLE_ID, LATEST_LINK_ID
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
        except ImportError as e:
            Log.instance().e("Modules not found. " + str(e))
            Log.instance().finish()
            raiserModuleNotFound(e)

    def getLatestVersionCode(self):
        aside = self.__soupObject.find(id=ASSIDE_ID)
        table = aside.find(id=TABLE_ID)
        td = table.find(id=LATEST_LINK_ID)
        html_latest_version = td.a
        # html_latest_version = self.__soupObject.find(id=FEATURED_ID).find(id=TABLE_ID).find(LATEST_LINK_ID).a
        return html_latest_version.get_text()

    def getLatestVersionURL(self):
        aside = self.__soupObject.find(id=ASSIDE_ID)
        table = aside.find(id=TABLE_ID)
        td = table.find(id=LATEST_LINK_ID)
        html_latest_link = td.a
        # html_latest_link = self.__soupObject.find(id=FEATURED_ID).find(id=TABLE_ID).find(LATEST_LINK_ID).a
        return html_latest_link.get('href')
