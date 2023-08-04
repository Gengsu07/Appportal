import datetime
import os
import webbrowser
import pyautogui as pg
import time
import glob
import shutil
import random
import pandas as pd

today = datetime.date.today()
download_path = r"C:\Users\810202558\Downloads"
baseDownloadedDir = r"D:\PROJECTS\Appportal\downloaded"
baseUrl = "https://appportal.intranet.pajak.go.id/portal/download/lsnfjkasbnfjnasjkfnjbnjnjknbkjnfjknbjkfnbkjfnbi3939489184.php?p1="
# kpp = ['001']
spm_baseUrl = "https://appportal.intranet.pajak.go.id/portal/spm/dataspmcsv.php?"


def generate_month_list():
    today = datetime.date.today()
    current_month = today.month
    months_list = [str(month).zfill(2) for month in range(1, current_month + 1)]
    return months_list


def create_folder(folder_name):
    try:
        os.mkdir(os.path.join("downloaded", folder_name))
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        pass


def delfiles(dir):
    try:
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")


def sorted_files(source_dir):
    csv_files = glob.glob(os.path.join(source_dir, "*.csv"))
    today_csv_files = []
    for csv_file in csv_files:
        stat = os.stat(csv_file)
        file_date = datetime.date.fromtimestamp(stat.st_ctime)
        if file_date == today:
            today_csv_files.append(csv_file)
    sorted_files = sorted(today_csv_files, key=os.path.getctime, reverse=False)
    return sorted_files


def moving_files(sorted_files, val):
    for filename in sorted_files:
        namefile = filename.split("\\")[-1]
        dest_dir = os.path.join(baseDownloadedDir, val, namefile)
        shutil.move(filename, dest_dir)


def etl_mpn(files):
    data_temp = pd.DataFrame()
    for file in files:
        namefile = (file.split("\\")[-1].split("_")[-1])[:3]
        temp = pd.read_csv(
            file,
            dtype={
                "NPWP": "str",
                "KPP": "str",
                "CAB": "str",
                "PTNTP": "str",
                "PTMSPJ": "str",
                "TGLBYR": "str",
                "BLNBYR": "str",
                "THNBYR": "str",
            },
        )
        temp["ADMIN"] = namefile
        data_temp = pd.concat([data_temp, temp], axis=0, ignore_index=True)

    data_temp.rename(
        columns={
            "THNBYR": "TAHUNBAYAR",
            "BLNBYR": "BULANBAYAR",
            "TGLBYR": "TANGGALBAYAR",
        },
        inplace=True,
    )
    data_temp["DATEBAYAR"] = (
        data_temp["TAHUNBAYAR"] + data_temp["BULANBAYAR"] + data_temp["TANGGALBAYAR"]
    )
    data_temp["DATEBAYAR"] = pd.to_datetime(data_temp["DATEBAYAR"], format="%Y%m%d")
    data_temp["MASA_PAJAK"] = data_temp["PTMSPJ"].str[0:2]
    data_temp["MASA_PAJAK2"] = data_temp["PTMSPJ"].str[2:4]
    data_temp["TAHUN_PAJAK"] = data_temp["PTMSPJ"].str[4:]
    return data_temp


def login():
    webbrowser.open("https://appportal.intranet.pajak.go.id/login/")
    time.sleep(2)
    pg.hotkey("tab")
    pg.typewrite("810202558", interval=0.1)
    pg.hotkey("tab")
    pg.typewrite("Gengsu!sh3r3", interval=0.1)
    pg.hotkey("enter")

    time.sleep(3)


def mpn(valuta, kpp, bulan):
    for val in valuta:
        mpn_dir = os.path.join(baseDownloadedDir, val)
        # bikin folder
        if not os.path.exists(mpn_dir):
            os.makedirs(mpn_dir)
        for adm in kpp:
            for bln in bulan:
                url = (
                    baseUrl + adm + tahun + jns_pajak + tgl_awal + tgl_akhir + bln + val
                )
                webbrowser.open_new_tab(url)
                if val == "1":
                    time.sleep(random.randint(2, 8))
                else:
                    time.sleep(random.randint(1, 3))

        mpn_sorted = sorted_files(download_path)
        num_files = len(kpp) * len(bulan)  # per valuta
        while len(mpn_sorted) < num_files:
            time.sleep(10)
            mpn_sorted = sorted_files(download_path)

        delfiles(mpn_dir)
        moving_files(mpn_sorted, val)

    url_usd = f"https://appportal.intranet.pajak.go.id/portal/detilperekaman/exportkpp.php?xunit=110&xtahun=2023&xbulan1=01&xbulan2={bulan[-1]}"
    webbrowser.open_new_tab(url_usd)
    time.sleep(3)
    shutil.move(
        os.path.join(download_path, "detildollar.xls"),
        r"D:\PROJECTS\Appportal\downloaded\2\detildollar.xls",
    )


def spm(baseUrl, kpp, bulan):
    spm_dir = os.path.join(baseDownloadedDir, "spm")
    # bikin folder
    if not os.path.exists(spm_dir):
        os.makedirs(spm_dir)
    ant = "&"
    placeholder = []
    for adm in kpp:
        for bln in bulan:
            url = (
                baseUrl
                + "p1="
                + tgl_awal
                + ant
                + "p2="
                + tgl_akhir
                + ant
                + "p3="
                + bln
                + ant
                + "p4="
                + tahun
                + ant
                + "p5="
                + adm
            )
            webbrowser.open_new_tab(url)
            time.sleep(random.randint(1, 3))
            namabaru = "\\SPM" + "_" + f"{adm}" + "_" + f"{bln}" + ".csv"
            placeholder.append(namabaru)
            # spm_downloaded = glob.glob(os.path.join(download_path, "Data_SPM*.csv"))
            # if len(spm_downloaded) > 0:
            #     namabaru = "\\SPM" + "_" + f"{adm}" + "_" + f"{bln}" + ".csv"
            #     os.rename(spm_downloaded[0], download_path + namabaru)
            # else:
            #     time.sleep(2)
            #     namabaru = "\\SPM" + "_" + f"{adm}" + "_" + f"{bln}" + ".csv"
            #     os.rename(spm_downloaded[0], download_path + namabaru)

    spm_sorted = sorted_files(download_path)
    num_files = len(kpp) * len(bulan)  # per va luta
    while len(spm_sorted) < num_files:
        time.sleep(10)
        spm_sorted = sorted_files(download_path)

    delfiles(spm_dir)
    for n, nama in enumerate(spm_sorted):
        parent_dir = nama.split("\\")
        parent_dir = "\\".join(x for x in parent_dir[:-1])
        os.rename(nama, parent_dir + placeholder[n])
    spm_sorted = sorted_files(download_path)
    moving_files(spm_sorted, "spm")


def etl_mpnspm(idr_files, usd_files, dolar_file, pbb_files, spm_files):
    idr_files = idr_files
    usd_files = usd_files
    dolar_file = dolar_file
    pbb_files = pbb_files
    spm_files = spm_files

    data_mpn = etl_mpn(idr_files)
    # data_mpn['DATEBAYAR'] = pd.to_datetime(data_mpn[['TANGGALBAYAR', 'BULANBAYAR', 'TAHUNBAYAR']])
    # USD
    data_usd = etl_mpn(usd_files)

    data_dollar = pd.read_excel(
        r"downloaded\2\detildollar.xls",
        engine="xlrd",
        usecols=["NTPN", "JUMLAH RUPIAH"],
    )
    data_usd = data_usd.merge(data_dollar, left_on="PTNTP", right_on="NTPN", how="left")
    data_usd = data_usd.drop(columns=["JUMLAH", "NTPN"])
    data_usd = data_usd.rename(columns={"JUMLAH RUPIAH": "JUMLAH"})

    data_pbb = etl_mpn(pbb_files)

    data_mpnall = pd.concat([data_mpn, data_usd], axis=0, ignore_index=False)
    data_mpnall = pd.concat([data_mpnall, data_pbb], axis=0, ignore_index=False)
    data_mpnall[["NOP", "KET"]] = data_mpnall[["NOP", "KET"]].fillna("-")
    data_mpnall.columns = [x.lower() for x in data_mpnall.columns]
    data_mpnall = data_mpnall.rename(
        columns={
            "cab": "cabang",
            "kjs": "kdbyar",
            "masa_pajak": "masa",
            "tahun_pajak": "tahun",
            "jumlah": "nominal",
            "ptntp": "ntpn",
            "noskssp": "nosk",
            "id": "billing",
            "pembuat billing": "pembuat",
            "masa_pajak2": "masa2",
        }
    )
    data_mpnall = data_mpnall.rename(columns={"kdbyar": "kdbayar"})
    data_mpnall["nospm"] = ""
    data_mpnall["source"] = 1
    data_mpnall["extra"] = ""
    data_mpnall["tipe"] = ""
    data_mpnall = data_mpnall.drop(columns=["alamat", "kd bank", "kpp_penerima"])
    data_mpnall = data_mpnall[
        [
            "admin",
            "npwp",
            "kpp",
            "cabang",
            "nama",
            "kdmap",
            "kdbayar",
            "masa",
            "tahun",
            "tanggalbayar",
            "bulanbayar",
            "tahunbayar",
            "datebayar",
            "nominal",
            "ntpn",
            "bank",
            "nosk",
            "nospm",
            "tipe",
            "source",
            "extra",
            "billing",
            "nop",
            "pembuat",
            "ket",
            "masa2",
        ]
    ]
    # SPM
    data_spm = pd.DataFrame()
    for csv_file in spm_files:
        namefile = (csv_file.split("_"))[1]
        spm_temp = pd.read_csv(
            csv_file,
            dtype={
                "MASA PAJAK": "str",
                "TANGGAL BAYAR": "str",
                "NPWP": "str",
                "KPP": "str",
                "CABANG": "str",
            },
        )
        spm_temp["ADMIN"] = namefile
        data_spm = pd.concat([data_spm, spm_temp], axis=0, ignore_index=True)
    data_spm["MASA PAJAK2"] = data_spm["MASA PAJAK"].str[2:3]
    data_spm["MASA PAJAK"] = data_spm["MASA PAJAK"].str[:2]
    data_spm.loc[data_spm["MASA PAJAK"] == "n", "MASA PAJAK"] = data_spm[
        "TANGGAL BAYAR"
    ].str[4:6]
    data_spm.loc[data_spm["MASA PAJAK"] == "n", "TAHUN PAJAK"] = data_spm[
        "TANGGAL BAYAR"
    ].str[:3]

    data_spm.loc[data_spm["MASA PAJAK"] != "n", "MASA PAJAK"] = data_spm[
        "MASA PAJAK"
    ].str[:1]
    data_spm.loc[data_spm["MASA PAJAK"] != "n", "TAHUN PAJAK"] = data_spm[
        "MASA PAJAK"
    ].str[4:]

    data_spm["DATEBAYAR"] = data_spm["TANGGAL BAYAR"].copy()
    data_spm["DATEBAYAR"] = pd.to_datetime(data_spm["DATEBAYAR"])
    data_spm["TAHUN_BAYAR"] = data_spm["TANGGAL BAYAR"].str[:4]
    data_spm["BULAN_BAYAR"] = data_spm["TANGGAL BAYAR"].str[4:6]
    data_spm["TANGGAL_BAYAR"] = data_spm["TANGGAL BAYAR"].str[6:]
    data_spm_fil = data_spm.filter(
        [
            "ADMIN",
            "NPWP",
            "KPP",
            "CABANG",
            "NAMA WAJIB PAJAK",
            "KODE MAP",
            "KODE BAYAR",
            "MASA_PAJAK",
            "TAHUN_PAJAK",
            "TANGGAL_BAYAR",
            "BULAN_BAYAR",
            "TAHUN_BAYAR",
            "DATEBAYAR",
            "JUMLAH BAYAR (Rp)",
            "NO SK SSP",
            "NTPN",
        ]
    )
    data_spm_fil = data_spm_fil.rename(
        columns={
            "NAMA WAJIB PAJAK": "NAMA",
            "KODE MAP": "KDMAP",
            "KODE BAYAR": "KJS",
            "JUMLAH BAYAR (Rp)": "JUMLAH",
            "NO SK SSP": "NOSK",
        }
    )
    data_spm_fil.BULAN_BAYAR = data_spm_fil.BULAN_BAYAR.astype("int")
    data_spm_fil["SOURCE"] = 1

    return [data_mpnall, data_spm_fil]


if __name__ == "__main__":
    # kpp = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "097"]
    kpp = ["001"]
    tahun = "2023"
    jns_pajak = "411100000"
    tgl_awal = "01"
    tgl_akhir = "31"
    bulan = generate_month_list()
    bulan = ["01"]
    valuta = ["1", "2", "3"]

    login()
    mpn(valuta, kpp, bulan)
    spm(spm_baseUrl, kpp, bulan)

    idr_files = glob.glob(r"downloaded\1\*.csv")
    usd_files = glob.glob(r"downloaded\2\*.csv")
    dolar_file = glob.glob(r"downloaded\2\*.xls")
    pbb_files = glob.glob(r"downloaded\3\*.csv")
    spm_files = glob.glob(r"downloaded\spm\*.csv")
    [data_mpn, data_spm] = etl_mpnspm(
        idr_files, usd_files, dolar_file, pbb_files, spm_files
    )
    data_mpn.to_excel(r"D:\HASILKUERI\mpn.xlsx", index=False)
    data_spm.to_excel(r"D:\HASILKUERI\spm.xlsx", index=False)
