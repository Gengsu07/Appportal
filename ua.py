# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(user_agent=userAgent)
#     page = context.new_page()
#     cookies = [
#         {
#             "name": "appportal",
#             "value": "BIGipServerappportal_pool=rd1217o00000000000000000000ffff0af50271o80; PHPSESSID=nr7ersa1mregj079cqrs51cp24; TS01dbe13e=01241cebe01e1e2716ceb102a8067c4c99c0595a8f6de13829bc3ed026e6eb9cb2d447f84c54556eb6250331fcf6c491e38ff39097860a63dc6aac96e86e8edb1050fbeea7b601a253334e6f2cd32424bc581870a9; TSPD_101=0825bdee18ab28005696d27f1d2d2ce6a80ec853c65fb5e1d88027768e7ff33a9a5792baaf7cf5ad668afd59bcaf0cd9080236f02205180093594778476af56397bb546fe0dd7b5e5ad0908de0c54489; TSb714f052027=0825bdee18ab2000800ed3a0ff44c0b51a78cdced5d82eeeaba26aed3253f3aa3cd911b652681ce0086425276111300058ca760bfab64557f7e95e4e1d6956581b0f05f9691428d49c6ce2194aa42862241a98adfc933e82f4d4f0241dff222e; TS00000000076=0825bdee18ab2800803a81490fc1a0927d43d93e0232af1e7a57fc8b3afb01606323c8d940802d402f5b7c5b4515835d088529c09a09d00050ff4eac04294b6115914d8d0761b013af058d1bad8569aee3ab972054a291710336859a8ba7e4971d93d14ea051157ed1b29b2e444cc4e387175b7526c070e2f0e134e21102c2962c38f4dcddd5e8e985094d9d8f2554f7ec1a2268c6e3ce8f7df5b48d8ccd49869cbb0e3d7d677873cf7a0ec1910ba61e28328495fdfc52f3860833b5f558b0124b27302ec236ac7d723d6b819881cd4623765aec4ccaa6539086c6c8c1c00b89ef115854acf06a75bb7d0ca4029d962ad412091e90340309848050fcfdc27fc8e7ba7cf2b0aa49c6; TSaab28764077=0825bdee18ab2800537a7f9e00e0033856618b007b32bd2246ffae4cbd19c1787e26ebed4c2336a1df8e37b81d7ecb2b080e957ad317200073cd5fdacd7711f051873270a7b4855c4d9a92dee51ac3dbaae3f729a45e1b11; TSPD_101_DID=0825bdee18ab2800803a81490fc1a0927d43d93e0232af1e7a57fc8b3afb01606323c8d940802d402f5b7c5b4515835d088529c09a063800c9b3b953342964f920e695ed314727bbf47a833c309c64f10ed9ff3f317240bac7fabf9a05b66a7adc701d112bd711503073cd41e1a5080e",
#             "domain": "appportal.intranet.pajak.go.id",
#         }
#     ]

#     page.set_cookies(cookies)
#     page.goto("https://appportal.intranet.pajak.go.id/login/")

#     # ---------------------
#     page.pause()
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time


opsi = Options()
opsi.add_argument("--headless")
# opsi.add_argument(f"user-agent={userAgent}")
# driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(service=ChromeDriverManager().install(), options=opsi)
try:
    url = "https://appportal.intranet.pajak.go.id/login"
    driver.get(url)
    print("Page title:", driver.title)  # Check the page title
    time.sleep(
        5
    )  # Wait for a few seconds to see the page (for demonstration purposes).
except Exception as e:
    print("An error occurred:", str(e))
finally:
    driver.quit()

time.sleep(2)
