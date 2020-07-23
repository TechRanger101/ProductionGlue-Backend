import time
from selenium.webdriver.common.keys import Keys
from amazon_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)


class GeneratedReport:
    def __init__(self):
        pass


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print('Stating script...')
        print(f'Looking for {self.search_term} products...')
        links = self.get_products_links()
        print(links)
        time.sleep(3)
        self.driver.quit()

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath(
            '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)  # wait to load
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)  # wait to load
        # result_list = self.driver.find_elements_by_class_name('s-result-list')

        links = []
        try:
            # results = result_list[0].find_elements_by_xpath(
            #     "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            results = self.driver.find_elements_by_xpath(
                '//a[@class = "a-link-normal s-no-outline"]')
            links = [link.get_attribute('href') for link in results]
            return links

        except Exception as e:
            print("Did'nt get any product....")
            print(e)
            return links


if __name__ == '__main__':
    print('HEY!!!')
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    amazon.run()
