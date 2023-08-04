from clicknium import clicknium as cc, locator, ui
import pyautogui as pag
import time


def pbk():
    tab = cc.chrome.attach_by_title_url(
        url='https://appportal.intranet.pajak.go.id/*')
    # tab = cc.chrome.open('https://appportal.intranet.pajak.go.id')
    # tab.wait_appear(locator.intranet.mpnharianrekon.text_username)
    # tab.find_element(locator.intranet.mpnharianrekon.text_username).set_text('810202558')
    # tab.find_element(locator.intranet.mpnharianrekon.password_password).set_text('Gengsu@110')
    # tab.wait_appear(locator.intranet.mpnharianrekon.submit_loginsub)
    # pag.click(x=1910, y=950, duration=1)
    tab.refresh()
    time.sleep(1)
    counter = 0
    pag.alert('Pergi ke halaman PBK dlu')
    # pag.confirm('Klik ')

    # pag.moveTo(x=190, y=210, duration=1)
    # pag.moveTo(x=199, y=260, duration=1)
    # pag.moveTo(x=370, y=260, duration=1)
    # pag.moveTo(x=370, y=400, duration=1)
    # time.sleep(1)
    # pag.click(x=370, y=400, duration=1)
    # pag.moveTo(x=700, y=650, duration=1)

    kpp = ['001', '002', '003', '004', '005',
           '006', '007', '008', '009', '097']
    for kantor in kpp:
        time.sleep(1)
        ui(locator.intranet.pbk.select_idkpp).click()
        time.sleep(1)
        pag.write(kantor, interval=0.2)
        time.sleep(1)
        pag.hotkey('enter')
        time.sleep(1)

        cc.find_element(locator.intranet.pbk.button_btncari).set_focus()
        tab.find_element(locator.intranet.pbk.button_btncari).click(
            mouse_button='left')
        time.sleep(1)
        cc.find_element(locator.intranet.pbk.button_csv).set_focus()
        tab.find_element(locator.intranet.pbk.button_csv).click(
            mouse_button='left')
        counter += 1
        # pag.click(x=1195, y=305, duration=1)
        # time.sleep(2)
        # pag.click(x=100, y=377, duration=1)
        time.sleep(3)
    print(f'PBK:{counter}')


if __name__ == '__main__':

    pbk()
