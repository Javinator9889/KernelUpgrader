from bs4 import BeautifulSoup
import requests


class Connection:
    KERNEL_PAGE = "https://www.kernel.org/"

    def __init__(self):
        saved_page_content = requests.get(self.KERNEL_PAGE).content
        self.soupObject = BeautifulSoup(saved_page_content, "lxml")

