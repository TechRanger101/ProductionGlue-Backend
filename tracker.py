from datetime import datetime
from logging import currentframe
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from amazon_config import *


class GeneratedReport:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        report = {
            'title': self.file_name,
            'date': self.getNow(),
            'currency': self.currency,
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        print("Creating report...")
        with open(f'{DIRECTORY}/{file_name}.json', 'w') as f:
            json.dump(report, f)
        print('Done...')

    def getNow(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = getWebDriverOptions()
        setIgnoreCertificateError(options)
        setBrowserAsIncognito(options)
        # makeHeadless(options)
        self.driver = getChromeWebDriver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print('Stating script...')
        print(f'Looking for {self.search_term} products...')
        links = self.getProductsLinks()
        time.sleep(1)
        if not links:
            print('Script Stopped.....!')
            return
        print(f'Got {len(links)} links to products....')
        print('Getting info about products....')
        products = self.getProductsInfo(links)
        self.driver.quit()
        return products

    def getProductsLinks(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath(
            '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)  # wait to load
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)  # wait to load

        links = []
        try:
            results = self.driver.find_elements_by_xpath(
                '//div[@class="a-section a-spacing-none"]/span/a')
            links = [link.get_attribute('href') for link in results]

        except Exception as e:
            print("Did'nt get any product....")
            print(e)

        return links

    def getProductsInfo(self, links):
        asins = self.getAsins(links)
        products = []
        for asin in asins:
            product = self.getSingleProductInfo(asin)
            if product:
                products.append(product)
        return products

    def getSingleProductInfo(self, asin):
        print(f"Product ID: {asin} - getting data....")
        product_short_url = self.shortenUrl(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.getTitle()
        seller = self.getSeller()
        price = self.getPrice()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def getTitle(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None

    def getSeller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(
                f"Can't get seller of the product - {self.driver.current_url}")
            return None

    def getPrice(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = self.convertPrice(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id(
                    'availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_xpath(
                        '//*[@class="olp-padding-right"]/span/font/font').text
                    price = price[price.find(self.currency):]
                    price = self.convertPrice(price)
            except Exception as e:
                print(e)
                print(
                    f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    def shortenUrl(self, asin):
        return self.base_url + 'dp/' + asin

    def getAsins(self, links):
        return [self.getAsin(link) for link in links]

    def getAsin(self, product_link):
        if '.html' in product_link:
            asin = product_link[product_link.find(
                '%2Fdp%2F')+8:product_link.find('%2Fref')]
        else:
            asin = product_link[product_link.find(
                '/dp/') + 4:product_link.find('/ref')]
        return asin

    def convertPrice(self, price):
        exp = " ," + self.currency
        for char in exp:
            price = price.replace(char, '')
        return float(price)


if __name__ == '__main__':
    print('HEY!!!')
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon.run()
    GeneratedReport(NAME, FILTERS, BASE_URL, CURRENCY,  data)
