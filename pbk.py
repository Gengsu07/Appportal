from clicknium import clicknium as cc, locator, ui
import pyautogui as pag
import time
from mpnspm import sorted_files, delfiles, moving_files
import os


def pbk(kpp, download_path, baseDownloadedDir):
    tab = cc.chrome.attach_by_title_url(url="https://appportal.intranet.pajak.go.id/*")

    tab.refresh()
    time.sleep(1)
    counter = 0
    pag.alert("Pergi ke halaman PBK dlu")
    kpp = kpp
    placeholder = []
    for kantor in kpp:
        time.sleep(1)
        ui(locator.intranet.pbk.select_idkpp).click()
        time.sleep(1)
        pag.write(kantor, interval=0.2)
        time.sleep(1)
        pag.hotkey("enter")
        time.sleep(1)

        cc.find_element(locator.intranet.pbk.button_btncari).set_focus()
        tab.find_element(locator.intranet.pbk.button_btncari).click(mouse_button="left")
        time.sleep(3)
        tab.find_element(locator.intranet.pbk.button_csv).wait_property(
            name="aria-controls", value="example"
        )
        cc.find_element(locator.intranet.pbk.button_csv).set_focus()
        tab.find_element(locator.intranet.pbk.button_csv).click(mouse_button="left")
        counter += 1
        namabaru = "\\PBK" + "_" + f"{kantor}" + ".csv"
        placeholder.append(namabaru)
        time.sleep(3)
    print(f"PBK:{counter}")
    pbk_sorted = sorted_files(download_path)
    num_files = len(kpp)  # per va luta
    if len(pbk_sorted) == num_files:
        pbk_dir = os.path.join(baseDownloadedDir, "pbk")
        # bikin folder
        if not os.path.exists(pbk_dir):
            os.makedirs(pbk_dir)
        delfiles(pbk_dir)
        for n, nama in enumerate(pbk_sorted):
            parent_dir = nama.split("\\")
            parent_dir = "\\".join(x for x in parent_dir[:-1])
            os.rename(nama, parent_dir + placeholder[n])
    pbk_sorted = sorted_files(download_path)
    moving_files(pbk_sorted, "pbk")


if __name__ == "__main__":
    pbk()
