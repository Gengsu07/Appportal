# from os import error
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import time
from bs4 import BeautifulSoup


opsi = Options()
opsi.add_argument("--headless=false")
# opsi.debugger_address = "127.0.0.1:9222"
# opsi.add_argument("download.default_directory= r'D:\PROJECTS\Appportal\mpn' ")

# opsi.add_argument("download.prompt_for_download= False")
# opsi.add_argument("download.directory_upgrade= True")
# opsi.add_argument("safebrowsing.enabled= True")
driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(driver_path, options=opsi)
ac = ActionChains(driver)
driver.get("https://appportal.intranet.pajak.go.id/login/")
time.sleep(2)
# driver.get(
#     "https://appportal.intranet.pajak.go.id/portal/download/lsnfjkasbnfjnasjkfnjbnjnjknbkjnfjknbjkfnbkjfnbi3939489184.php?p1=00120234111000000131072"
# )

# datapenerimaan = driver.find_element(By.XPATH, '//li[@style="z-index: 99;"]')
# ac.move_to_element(datapenerimaan).perform()
# time.sleep(1)
# mpn = driver.find_element(By.XPATH, '//*[@id="smoothmenu1"]/ul/li[2]/ul/li[2]/a')
# ac.move_to_element(mpn).perform()
# time.sleep(1)
# driver.find_element(By.XPATH, '//span[@id="mpnharianrekon2022"]').click()
# random_elemen = driver.find_element(By.CSS_SELECTOR, ".panel-heading")
# ac.move_to_element(random_elemen).perform()


# n_valuta = range(3)
# n_unit = range(10)
# n_bulan = range(datetime.date.today().month)

# time.sleep(2)
# for val in n_valuta:
#     valuta = Select(driver.find_element(By.CSS_SELECTOR, "#valuta"))
#     valuta.select_by_index(val)
#     time.sleep(1)
#     for kpp in n_unit:
#         unit = Select(driver.find_element(By.CSS_SELECTOR, "#dd_kppdankanwil"))
#         unit.select_by_index(kpp)
#         tgl_akhir = Select(driver.find_element(By.CSS_SELECTOR, "#tgl_akhir"))
#         tgl_akhir.select_by_index(30)
#         time.sleep(1)

#         for bln in n_bulan:
#             bulan = Select(driver.find_element(By.CSS_SELECTOR, "#bln_awal"))
#             bulan.select_by_index(bln)
#             # click download
#             driver.find_element(By.CSS_SELECTOR, "#btnDownload").click()
#             download = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, "#download > a:nth-child(1)")
#                 )
#             )
#             time.sleep(1)
#             download.click()
#             time.sleep(1)
driver.quit()
