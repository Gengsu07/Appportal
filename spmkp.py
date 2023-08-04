from clicknium import clicknium as cc, locator, ui
import pyautogui as pag
import time


def press_tab(y):
    for n in range(y):
        pag.hotkey("tab", interval=1)


def spmkp():
    tab = cc.chrome.attach_by_title_url(url="https://appportal.intranet.pajak.go.id/*")
    # tab = cc.chrome.open('https://appportal.intranet.pajak.go.id')
    # tab.wait_appear(locator.intranet.mpnharianrekon.text_username)
    # tab.find_element(locator.intranet.mpnharianrekon.text_username).set_text('810202558')
    # tab.find_element(locator.intranet.mpnharianrekon.password_password).set_text('Gengsu@110')
    # tab.wait_appear(locator.intranet.mpnharianrekon.submit_loginsub)
    # pag.click(x=1910, y=950, duration=1)
    tab.refresh()
    counter = 0

    # pag.moveTo(x=209, y=210, duration=1)
    # pag.moveTo(x=209, y=235, duration=1)
    # pag.click(x=220, y=235, duration=1)
    time.sleep(2)
    ui(locator.intranet.appportal.a_data_penerimaan).click()
    time.sleep(1)
    pag.hotkey("tab")
    pag.hotkey("enter")
    # ui(locator.intranet.appportal.a_monitoring_spmkp).click()
    # time.sleep(2)
    # menu spmkp
    time.sleep(1)

    ui(locator.intranet.spmkp.select_action).select_item(
        " Data Dashboard (SPMKP + SPMPP)"
    )
    # cc.find_element(locator.intranet.spmkp.button_btncari).set_focus()
    # tab.find_element(locator.intranet.spmkp.button_btncari).click(mouse_button='left')
    # time.sleep(1)
    # cc.find_element(locator.intranet.spmkp.button_csv).set_focus()
    # tab.find_element(locator.intranet.spmkp.button_csv).click(mouse_button='left')
    # counter +=1
    # pag.click(x=1181, y=305, duration=1)
    # time.sleep(1)
    # pag.click(x=105, y=376, duration=1)

    time.sleep(1)

    kpp = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "097"]
    # koordinat = [350, 370, 385, 405, 435, 455, 475, 490]
    for kantor in kpp:
        download(kantor, tab)
        counter += 1
    print(f"SPMKP:{counter}")


def download(y, tab):
    # pag.click(x=700, y=300, duration=1)
    # pag.click(x=700, y=y, duration=1)

    time.sleep(1)
    ui(locator.intranet.spmkp.select_dd_kppdankanwilplus).click()
    time.sleep(1)

    # press_tab(y)
    # pag.press('down', presses=y, interval=1)
    pag.write(y, interval=0.5)
    time.sleep(1)
    pag.hotkey("enter")
    # ui(locator.intranet.spmkp.select_dd_kppdankanwilplus).send_hotkey(
    #     '{ENTER}')
    time.sleep(1)
    cc.find_element(locator.intranet.spmkp.button_btncari).set_focus()
    tab.find_element(locator.intranet.spmkp.button_btncari).click(mouse_button="left")
    time.sleep(2)
    cc.find_element(locator.intranet.spmkp.button_csv).set_focus()
    tab.find_element(locator.intranet.spmkp.button_csv).click(mouse_button="left")
    print(y)
    time.sleep(2)


if __name__ == "__main__":
    spmkp()
