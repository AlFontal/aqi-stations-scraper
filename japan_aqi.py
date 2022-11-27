import os
import shutil
import logging
import requests
import geckodriver_autoinstaller

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()
geckodriver_autoinstaller.install()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('.last_attempt.log')
fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(message)s'))
logger.addHandler(fh)

japan_stations_url = 'https://aqicn.org/map/japan/'
my_name = os.environ['USER_FULL_NAME']
my_org = os.environ['USER_ORGANIZATION']
my_email = os.environ['USER_EMAIL']
download_folder = 'tmp_downloads'
data_folder = 'data/japan-aqi'

if os.path.exists(download_folder):
    shutil.rmtree(download_folder)
os.mkdir(download_folder)
page = requests.get(japan_stations_url)
soup = BeautifulSoup(page.content, 'html.parser')

stations_list = []
for station_link in soup.find(id='map-stations').find_all('a'):
    stations_list.append(station_link.text.split(' (')[0])

options = webdriver.FirefoxOptions()
options.headless = True
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir",
                       os.path.join(os.getcwd(), download_folder))
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
driver = webdriver.Firefox(options=options)


def download_station_data(driver: webdriver, station: str, sleep_time : int = 1):
    w, h = driver.get_window_size().values()
    station_without_non_ascii = station.encode("ascii", "ignore").decode()
    driver.get('https://aqicn.org/data-platform/register/')
    historic_div = driver.find_element(By.ID, 'historic-aqidata')
    driver.execute_script("return arguments[0].scrollIntoView();", historic_div)
    driver.execute_script(f"window.scrollBy(0, -{h/2});")
    station_prompt = historic_div.find_element(By.CLASS_NAME,'prompt')
    station_prompt.send_keys(station_without_non_ascii)
    sleep(sleep_time)
    search_result = historic_div.find_element(By.CLASS_NAME, 'result')
    driver.execute_script("return arguments[0].scrollIntoView();", search_result)
    driver.execute_script(f"window.scrollBy(0, -{h/2});")
    search_result.click()
    sleep(sleep_time) 
    download_button = driver.find_element(By.CLASS_NAME, 'ui.large.primary.button')
    download_button.click()
    sleep(sleep_time * 2)
    three_inputs = driver.find_element(By.CLASS_NAME, 'three.fields')
    three_inputs.find_element(By.NAME, 'name').send_keys(my_name)
    three_inputs.find_element(By.NAME, 'email').send_keys(my_email)
    three_inputs.find_element(By.NAME, 'organization').send_keys(my_org)
    terms = driver.find_element(By.NAME, 'terms')
    driver.execute_script("return arguments[0].scrollIntoView();", terms)
    driver.execute_script(f"window.scrollBy(0, -{h/2});")
    terms.click()    
    submit_button = driver.find_element(By.CLASS_NAME, 'ui.submit.button.primary')
    driver.execute_script("return arguments[0].scrollIntoView();", submit_button)
    driver.execute_script(f"window.scrollBy(0, -{h/2});")
    submit_button.click()
    sleep(sleep_time * 3)


for station in stations_list:
    try:
        download_station_data(driver, station, sleep_time=2)
        logger.info(msg=f'{station} data correctly downloaded')
    except Exception as e:
        logger.info(msg=
        f"{station} data couldn't be fetched: {e}, retrying with higher wait time"
        )
        try:
            download_station_data(driver, station, sleep_time=4)
            logger.info(msg=f'{station} data correctly downloaded')

        except Exception as e:
            logger.info(msg=f"{station} data couldn't be fetched: {e}")

for file in os.listdir(download_folder):
    shutil.move(os.path.join(download_folder, file),
                os.path.join(data_folder, file))

driver.close()
