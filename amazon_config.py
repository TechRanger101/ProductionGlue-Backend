from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'ps4'
CURRENCY = '€'
MIN_PRICE = '275'
MAX_PRICE = '650'
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}

BASE_URL = "http://www.amazon.de/"


def getChromeWebDriver(options):
    return webdriver.Chrome('./chromedriver/chromedriver.exe', chrome_options=options)


def getWebDriverOptions():
    return webdriver.ChromeOptions()


def setIgnoreCertificateError(options):
    options.add_argument('--ignore-certificate-errors')


def setBrowserAsIncognito(options):
    options.add_argument('--incognito')


def makeHeadless(options):
    options.add_argument('--headless')
