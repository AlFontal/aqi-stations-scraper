import os
import logging
import requests
import geckodriver_autoinstaller

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

geckodriver_autoinstaller.install()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('.last_attempt.log')
fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(message)s'))
logger.addHandler(fh)

japan_stations_url = 'https://aqicn.org/map/japan/'
my_name = 'Alejandro Fontal'
my_org = 'ISGlobal'
my_email = 'alejandro.fontal@isglobal.org'
download_folder = 'data/japan-aqi'


page = requests.get(japan_stations_url)
soup = BeautifulSoup(page.content, 'html.parser')

stations_list = []
for station_link in soup.find(id='map-stations').find_all('a'):
    stations_list.append(station_link.text.split(' (')[0])

options = webdriver.FirefoxOptions()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), download_folder))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
driver = webdriver.Firefox(firefox_profile=profile)


def download_station_data(driver: webdriver, station: str, sleep_time : int = 1):
    station_without_non_ascii = station.encode("ascii", "ignore").decode()
    driver.get('https://aqicn.org/data-platform/register/')
    historic_div = driver.find_element_by_id('historic-aqidata')
    driver.execute_script("return arguments[0].scrollIntoView();", historic_div)
    driver.execute_script("window.scrollBy(0, -150);")
    station_prompt = historic_div.find_element_by_class_name('prompt')
    station_prompt.send_keys(station_without_non_ascii)
    sleep(sleep_time)
    search_result = historic_div.find_element_by_class_name('result')
    search_result.click()
    sleep(sleep_time)
    download_button = driver.find_element_by_class_name('ui.large.primary.button')
    download_button.click()
    sleep(sleep_time * 2)
    three_inputs = driver.find_element_by_class_name('three.fields')
    driver.execute_script("return arguments[0].scrollIntoView();", three_inputs)
    three_inputs.find_element_by_name('name').send_keys(my_name)
    three_inputs.find_element_by_name('email').send_keys(my_email)
    three_inputs.find_element_by_name('organization').send_keys(my_org)
    driver.find_element_by_name('terms').click()
    submit_button = driver.find_element_by_class_name('ui.submit.button.primary')
    submit_button.click()
    sleep(sleep_time * 3)


for station in stations_list:
    try:
        download_station_data(driver, station, sleep_time=2)
        logger.info(msg=f'{station} data correctly downloaded')
    except Exception as e:
        logger.info(msg=f"{station} data couldn't be fetched: {e}, retrying with higher wait time")
        try:
            download_station_data(driver, station, sleep_time=4)
        except Exception as e:
            logger.info(msg=f"{station} data couldn't be fetched: {e}")

driver.close()
