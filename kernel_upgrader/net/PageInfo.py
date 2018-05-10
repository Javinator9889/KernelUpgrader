import logging

from kernel_upgrader.values.Constants import (
    WI_KERNEL_PAGE,
    WI_PARSER,
    WI_ASSIDE_ID,
    WI_TABLE_ID,
    WI_LATEST_LINK_ID,
    LOG_KERNEL)
from kernel_upgrader.exceptions import raiserModuleNotFound


class Connection:
    def __init__(self):
        try:
            from bs4 import BeautifulSoup
            import lxml
            import requests
            saved_page_content = requests.get(WI_KERNEL_PAGE).content
            self.__soupObject = BeautifulSoup(saved_page_content, WI_PARSER)
        except ImportError as e:
            logging.getLogger(LOG_KERNEL).error("Modules not found. " + str(e))
            raiserModuleNotFound(e)

    def getLatestVersionCode(self):
        aside = self.__soupObject.find(id=WI_ASSIDE_ID)
        table = aside.find(id=WI_TABLE_ID)
        td = table.find(id=WI_LATEST_LINK_ID)
        html_latest_version = td.a
        return html_latest_version.get_text()

    def getLatestVersionURL(self):
        aside = self.__soupObject.find(id=WI_ASSIDE_ID)
        table = aside.find(id=WI_TABLE_ID)
        td = table.find(id=WI_LATEST_LINK_ID)
        html_latest_link = td.a
        return html_latest_link.get('href')
