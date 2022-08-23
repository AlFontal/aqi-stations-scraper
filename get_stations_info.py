import pandas as pd
from tqdm.auto import tqdm
import geckodriver_autoinstaller

from glob import glob
from time import sleep
from selenium import webdriver
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()
geckodriver_autoinstaller.install()
options = webdriver.FirefoxOptions()
options.headless = True
stations = [s.split('/')[-1][:-16] for s in glob('data/japan-aqi/*.csv')]


def get_directions_info(stations: list, options=None) -> pd.DataFrame:
    """
    Takes a list of directions and returns a dataframe with information about coordinates, and 
    location (address, zipcode city, county, state, country) using the geocode finder tool 
    (https://www.mapdevelopers.com/geocode_tool.php).
    """
    
    if options is None:
        options = webdriver.FirefoxOptions()
        options.headless = True

    driver = webdriver.Firefox(options=options)
    directions_info = defaultdict(list)
    for i, station in tqdm(enumerate(stations), desc='Getting stations info', total=len(stations)):
        if i % 100 == 0:
            driver.get('https://www.mapdevelopers.com/geocode_tool.php')
            sleep(10)
            text_field = driver.find_element_by_class_name('form-control')
            find_button = driver.find_elements_by_xpath("//*[contains(text(), 'Find Address')]")[0]
        text_field.clear()
        text_field.send_keys(station)
        find_button.click()
        sleep(2)
        try: 
            lat = driver.find_elements_by_id('display_lat')[0].text
        except ValueError:
            sleep(4)
            lat = driver.find_elements_by_id('display_lat')[0].text
        lon = driver.find_elements_by_id('display_lng')[0].text
        directions_info['address'].append(driver.find_elements_by_id('display_address')[0].text)
        directions_info['state'].append(driver.find_elements_by_id('display_state')[0].text)
        directions_info['city'].append(driver.find_elements_by_id('display_city')[0].text)
        directions_info['zipcode'].append(driver.find_elements_by_id('display_zip')[0].text)
        directions_info['county'].append(driver.find_elements_by_id('display_county')[0].text)
        directions_info['country'].append(driver.find_elements_by_id('display_country')[0].text)
        directions_info['coordinates'].append((lat, lon))

    driver.quit()
    
    return pd.DataFrame(directions_info) 


if __name__ == '__main__':

    directions_info = get_directions_info(stations)
    directions_info.to_csv('data/japan-aqi/directions_info.csv', index=False)