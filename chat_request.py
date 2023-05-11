
import bs4
import urllib
#import requests
from bs4 import BeautifulSoup as soup



#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import os

from joblib import Parallel, delayed
from multiprocessing import Pool
import threading

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

import zipfile

#PROXY_HOST = '117.208.148.72'  # rotating proxy or host
#PROXY_PORT = 3128 # port
PROXY_HOST = 'proxy.sarkar.icu'  # rotating proxy or host
PROXY_PORT = 8888 # port
PROXY_USER = 'shirley' # username
PROXY_PASS = 'hoenieseeteeT4n' # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

lock = threading.Lock()

def get_chromedriver(dis, pol, use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_experimental_option("detach", True)
    path = 'F:\\chat\\2022\\' + dis + '\\' + pol #change
    prefs = {'download.default_directory' : path, 'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome('C:\\Users\\schen\\OneDrive\\Desktop\\code\\chromedriver', chrome_options=chrome_options)
    return driver

def to_str(d1):
    year = d1.year
    month = d1.month
    day = d1.day

    str_date = str(day).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year)
    return str_date

#def download_all(station_n, start, num_pages):
def download_all(info):
    dis = info[0]
    pol = info[1]
    start = info[2]
    lock.acquire()
    path = os.path.join("F:\\chat\\2022\\", dis) #change
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, pol)
    if not os.path.exists(path):
        os.mkdir(path)
    lock.release()
    base_url = 'http://search.cgpolice.gov.in/CCTNS_Citizen_Portal/Citizen_Portal.jsp'
    driver = get_chromedriver(dis, pol, use_proxy=True)
    driver.get(base_url)

    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='33301']")))
    time.sleep(1)

    district = Select(driver.find_element_by_id("dist"))
    district.select_by_value(dis)
    time.sleep(5)

    pol_select = Select(driver.find_element_by_id("station"))
    pol_select.select_by_value(pol)
    time.sleep(2)
    from_date = driver.find_element_by_id("fromDt")
    driver.execute_script("arguments[0].removeAttribute('readonly', 'readonly')", from_date)
    from_date.clear()

    d1 = datetime.date(2022, 12, 1) #change
    d1_str = to_str(d1)
    from_date.send_keys(d1_str)
    time.sleep(1)
    
    driver.find_element_by_class_name("col-sm-2").click()
    time.sleep(2)
    buttons = driver.find_elements_by_class_name("btn-default")
    search = buttons[0]
    search.click()
    time.sleep(2)
    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.ID,"bdycontent")))


    test = True #check if the police station has any firs
    page_soup = soup(driver.page_source, 'html.parser')
    row = page_soup.find_all("tr", {"class": "success"})
    while(len(row) == 0): #if no reports in december, iterate backwards
        new_month = d1.month - 1
        if new_month < 1:
            test = False
            break
        d1 = d1.replace(month=new_month)
        from_date = driver.find_element_by_id("fromDt")
        driver.execute_script("arguments[0].removeAttribute('readonly', 'readonly')", from_date)
        from_date.clear()
        d1_str = to_str(d1)
        from_date.send_keys(d1_str)
        time.sleep(1)
        driver.find_element_by_class_name("col-sm-2").click()
        time.sleep(4)
        buttons = driver.find_elements_by_class_name("btn-default")
        search = buttons[0]
        search.click()
        time.sleep(1)
        WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.ID,"bdycontent")))
        page_soup = soup(driver.page_source, 'html.parser')
        row = page_soup.find_all("tr", {"class": "success"})
    

    page_soup = soup(driver.page_source, 'html.parser')
    row = page_soup.find_all("tr", {"class": "success"})

    if test == True:
        elems = row[0].find_all("td")
        max = elems[0].text.split("/")[0]
        print(max)
        for i in range(start, int(max) + 1):
            param = str(pol) + "22" + str(i).zfill(4) #change
            url_param = "http://search.cgpolice.gov.in/CCTNS_Citizen_Portal/WriteServlet?param=" + param
            pdf_path = "D:\\2022\\" + dis + "\\" + pol + "\\" + param + ".pdf" #change
            if os.path.exists(pdf_path) is False:
                try:
                    driver.get(url_param)
                except WebDriverException:
                    print("no fir")
            filename = "C:\\Users\\schen\\OneDrive\\Desktop\\code\\info_request\\" + dis + "\\" + pol + ".txt"
            f = open(filename, "a")
            text = "\n" + str(i) 
            f.write(text)
            f.close()
    filename = "C:\\Users\\schen\\OneDrive\\Desktop\\code\\info_request\\" + dis + "\\" + pol + ".txt"

    os.remove(filename)
    time.sleep(60)
    driver.quit()

info = {



 
#('33309', '33309046', 1), ('33309', '33309052', 1), ('33309', '33309074', 1)
#__________________


 
('33365', '33360001', 1), ('33365', '33360002', 1), ('33365', '33360004', 1), ('33365', '33360006', 1), ('33365', '33360007', 1), ('33365', '33360009', 1),

('33366', '33363004', 1), ('33366', '33363005', 1), ('33366', '33363006', 1), ('33366', '33363008', 1), ('33366', '33363012', 1), ('33366', '33363015', 1), ('33366', '33363020', 1), ('33366', '33363027', 1), ('33366', '33363031', 1), ('33366', '33363032', 1), ('33366', '33363065', 1), ('33366', '33366006', 1), ('33366', '33366047', 1),

('33368', '33368048', 1),

('33811', '33811008', 1), ('33811', '33811060', 1),
('33816', '33816011', 1),

('33820', '33820003', 1), ('33820', '33820004', 1),

('33821', '33821006', 1),
('33822', '33822007', 1)
}
                
#http://search.cgpolice.gov.in/CCTNS_Citizen_Portal/WriteServlet?param=33305003220038
#station number, year, fir


if __name__ == '__main__':
	p = Pool(8)
	p.map(download_all, info) #use multithreading for each page retrieval and parsing
	p.terminate()
	p.join()
#
	#multi_download = Parallel(n_jobs=4)(delayed(download_all)(key) for key in info)
   # download_all()
