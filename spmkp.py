from clicknium import clicknium as cc, locator, ui
import pyautogui as pag
import time
import os
from mpnspm import moving_files, sorted_files, delfiles


def press_tab(y):
    for n in range(y):
        pag.hotkey("tab", interval=1)


def spmkp(kpp, download_path, baseDownloadedDir):
    tab = cc.chrome.attach_by_title_url(url="https://appportal.intranet.pajak.go.id/*")

    tab.refresh()
    counter = 0
    time.sleep(1)
    tab.find_element(locator.intranet.appportal.a_data_penerimaan).wait_property(
        name="class", value="downarrowclass"
    )
    time.sleep(1)
    # ui(locator.intranet.appportal.a_data_penerimaan).click()
    # time.sleep(1)
    # pag.hotkey("tab")
    # pag.hotkey("enter")
    pag.alert("Pergi ke halaman SPMKP dlu")

    time.sleep(1)

    ui(locator.intranet.spmkp.select_action).select_item(
        " Data Dashboard (SPMKP + SPMPP)"
    )

    time.sleep(1)

    kpp = kpp
    placeholder = []
    for kantor in kpp:
        download(kantor, tab)
        counter += 1
        namabaru = "\\SPMKP" + "_" + f"{kantor}" + ".csv"
        placeholder.append(namabaru)
    print(f"SPMKP:{counter}")

    spmkp_sorted = sorted_files(download_path)
    num_files = len(kpp)  # per va luta
    if len(spmkp_sorted) == num_files:
        spmkp_dir = os.path.join(baseDownloadedDir, "spmkp")
        # bikin folder
        if not os.path.exists(spmkp_dir):
            os.makedirs(spmkp_dir)
        delfiles(spmkp_dir)
        for n, nama in enumerate(spmkp_sorted):
            parent_dir = nama.split("\\")
            parent_dir = "\\".join(x for x in parent_dir[:-1])
            os.rename(nama, parent_dir + placeholder[n])
    spmkp_sorted = sorted_files(download_path)
    moving_files(spmkp_sorted, "spmkp")


def download(y, tab):
    time.sleep(1)
    ui(locator.intranet.spmkp.select_dd_kppdankanwilplus).click()
    time.sleep(1)

    pag.write(y, interval=0.1)
    time.sleep(1)
    pag.hotkey("enter")
    time.sleep(1)
    cc.find_element(locator.intranet.spmkp.button_btncari).set_focus()
    tab.find_element(locator.intranet.spmkp.button_btncari).click(mouse_button="left")
    tab.find_element(locator.intranet.spmkp.button_csv).wait_property(
        name="aria-controls", value="example"
    )
    cc.find_element(locator.intranet.spmkp.button_csv).set_focus()
    tab.find_element(locator.intranet.spmkp.button_csv).click(mouse_button="left")

    time.sleep(2)


if __name__ == "__main__":
    spmkp()
