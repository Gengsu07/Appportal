import datetime
import os
import webbrowser
import pyautogui as pg
import time
import glob
import shutil
import random
from clicknium import clicknium as cc, locator
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("APPPORTAL_USERNAME")
password = os.getenv("APPPORTAL_PASSWORD")
from sqlalchemy import create_engine

masterfile_con = create_engine("mysql://root@localhost/registrasi".format("sgwi2341"))

today = datetime.date.today()
# download_path = r"C:\Users\810202558\Downloads"
download_path = r"C:\Users\sugengw07\Downloads"
# baseDownloadedDir = r"D:\PROJECTS\Appportal\downloaded"
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
                "KDMAP": "int",
                "kjs": "int",
                "PTNTP": "str",
                "PTMSPJ": "str",
                "TGLBYR": "str",
                "BLNBYR": "str",
                "THNBYR": "str",
            },
        )
        temp["ADMIN"] = namefile
        data_temp = pd.concat([data_temp, temp], axis=0, ignore_index=True)
    data_temp = data_temp.drop(columns=["ALAMAT", "KD BANK", "KPP_PENERIMA"])
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
    data_temp[
        ["TAHUNBAYAR", "BULANBAYAR", "TANGGALBAYAR", "KJS", "JUMLAH"]
    ] = data_temp[["TAHUNBAYAR", "BULANBAYAR", "TANGGALBAYAR", "KJS", "JUMLAH"]].apply(
        lambda x: pd.to_numeric(x, downcast="integer")
    )
    data_temp["MASA_PAJAK"] = (data_temp["PTMSPJ"].str[0:2]).astype("int")
    data_temp["MASA_PAJAK2"] = (data_temp["PTMSPJ"].str[2:4]).astype("int")
    data_temp["TAHUN_PAJAK"] = (data_temp["PTMSPJ"].str[4:]).astype("int")
    return data_temp


def login():
    webbrowser.open("https://appportal.intranet.pajak.go.id/login/")
    time.sleep(3)
    tab = cc.chrome.attach_by_title_url(url="https://appportal.intranet.pajak.go.id/*")
    tab.find_element(locator.intranet.appportal.submit_loginsub).wait_property(
        name="value", value="Login"
    )
    time.sleep(1)
    pg.hotkey("tab")
    pg.write(username, interval=0.1)
    pg.hotkey("tab")
    pg.write(password, interval=0.1)
    pg.hotkey("enter")
    tab.find_element(locator.intranet.appportal.a_data_penerimaan).wait_property(
        name="class", value="downarrowclass"
    )


def mpn(valuta, kpp, bulan, tahun, jns_pajak, tgl_awal, tgl_akhir):
    for val in valuta:
        print(f"downlaod mpn:{val} mulai")
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
                    time.sleep(random.randint(2, 4))
                else:
                    time.sleep(random.randint(1, 3))
        print(f"download mpn:{val} selesai")
        time.sleep(5)
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
    dollar = os.path.join(download_path, "detildollar.xls")
    if os.path.exists(dollar):
        print("download dollar selesai")
        shutil.move(
            os.path.join(download_path, "detildollar.xls"),
            os.path.join(baseDownloadedDir, "2", "detildollar.xls"),
        )
    else:
        time.sleep(5)
        if os.path.exists(dollar):
            print("download dollar selesai")
            shutil.move(
                os.path.join(download_path, "detildollar.xls"),
                os.path.join(baseDownloadedDir, "2", "detildollar.xls"),
            )


def spm(baseUrl, kpp, bulan, tgl_awal, tgl_akhir, tahun):
    spm_dir = os.path.join(baseDownloadedDir, "spm")
    # bikin folder
    if not os.path.exists(spm_dir):
        os.makedirs(spm_dir)
    ant = "&"
    placeholder = []
    print(f"download spm mulai")
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
            time.sleep(random.randint(3, 5))
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
        print(f"download spm {adm} selesai")
    time.sleep(5)
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
    # USD

    data_dollar = pd.read_excel(
        r"downloaded\2\detildollar.xls",
        engine="xlrd",
        dtype={"MASA": "str", "NPWP": "str", "KPP": "str", "CAB": "str"},
    )
    data_dollar["TANGGAL SETOR"] = pd.to_datetime(
        data_dollar["TANGGAL SETOR"], dayfirst=True
    )
    data_dollar["TAHUNBAYAR"] = data_dollar["TANGGAL SETOR"].dt.year
    data_dollar["BULANBAYAR"] = data_dollar["TANGGAL SETOR"].dt.month
    data_dollar["TANGGALBAYAR"] = data_dollar["TANGGAL SETOR"].dt.day
    data_dollar["MASA_PAJAK"] = data_dollar["MASA"].str[:2]
    data_dollar["MASA_PAJAK2"] = data_dollar["MASA"].str[2:4]
    data_dollar["TAHUN_PAJAK"] = data_dollar["MASA"].str[4:]

    dollar_rename = {
        "NAMA WAJIB PAJAK": "NAMA",
        "MAP": "KDMAP",
        "KD.SETOR": "KJS",
        "JUMLAH RUPIAH": "JUMLAH",
        "MASA": "PTMSPJ",
        "NTPN": "PTNTP",
        "TANGGAL SETOR": "DATEBAYAR",
        "NO KETETAPAN": "NOSKSSP",
    }
    data_dollar.rename(columns=dollar_rename, inplace=True)
    data_dollar["NPWP"] = data_dollar["NPWP"].str.strip()
    data_dollar["NPWP15"] = (
        data_dollar["NPWP"] + data_dollar["KPP"] + data_dollar["CAB"]
    )
    data_dollar["BANK"] = ""
    data_dollar["ID"] = ""
    data_dollar["NOP"] = ""
    data_dollar["PEMBUAT BILLING"] = ""
    data_dollar["KET"] = ""
    filter_npwp = ",".join([f"'{x.strip()}'" for x in data_dollar["NPWP15"].unique()])

    mf_kueri = f"""select KPPADM,NPWP15 from registrasi.sidjp_masterfile where NPWP15 in({filter_npwp})"""
    mf = pd.read_sql(mf_kueri, con=masterfile_con)
    data_dollar = data_dollar.merge(mf, on="NPWP15", how="left")
    data_dollar.rename(columns={"KPPADM": "ADMIN"}, inplace=True)
    data_dollar.drop(columns=["NPWP15"], inplace=True)
    data_dollar = data_dollar[data_mpn.columns]

    data_pbb = etl_mpn(pbb_files)

    data_mpnall = pd.concat([data_mpn, data_dollar], axis=0, ignore_index=False)
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
    # data_mpnall["extra"] = ""
    # data_mpnall["tipe"] = ""
    mpnspm_columns = [
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
        "source",
        "billing",
        "nop",
        "pembuat",
        "ket",
        "masa2",
    ]
    data_mpnall = data_mpnall[mpnspm_columns]
    # SPM
    data_spm = pd.DataFrame()
    for csv_file in spm_files:
        namefile = (csv_file.split("_"))[1]
        spm_temp = pd.read_csv(
            csv_file,
            dtype={
                "MASA PAJAK": "str",
                "KODE BANK": "str",
                "TANGGAL BAYAR": "str",
                "NPWP": "str",
                "KPP": "str",
                "CABANG": "str",
                "NTPN": "str",
                "NO SPM": "str",
            },
        )
        spm_temp["ADMIN"] = namefile
        data_spm = pd.concat([data_spm, spm_temp], axis=0, ignore_index=True)
    data_spm["MASA PAJAK2"] = data_spm["MASA PAJAK"].str[2:4]
    data_spm["TAHUN"] = data_spm["MASA PAJAK"].str[-4:]
    data_spm["MASA PAJAK"] = data_spm["MASA PAJAK"].str[:2]
    data_spm["DATEBAYAR"] = data_spm["TANGGAL BAYAR"].copy()
    data_spm["DATEBAYAR"] = pd.to_datetime(data_spm["DATEBAYAR"], yearfirst=True)
    data_spm["TAHUNBAYAR"] = data_spm["TANGGAL BAYAR"].str[:4]
    data_spm["BULANBAYAR"] = data_spm["TANGGAL BAYAR"].str[4:6]
    data_spm["TANGGALBAYAR"] = data_spm["TANGGAL BAYAR"].str[6:]
    data_spm_fil = data_spm.filter(
        [
            "ADMIN",
            "NPWP",
            "KPP",
            "CABANG",
            "NAMA WAJIB PAJAK",
            "KODE MAP",
            "KODE BAYAR",
            "MASA PAJAK",
            "MASA PAJAK2",
            "TAHUN",
            "TANGGALBAYAR",
            "BULANBAYAR",
            "TAHUNBAYAR",
            "DATEBAYAR",
            "JUMLAH BAYAR (Rp)",
            "NO SPM",
            "NO SK SSP",
            "NTPN",
            "KODE BANK",
        ]
    )
    data_spm_fil = data_spm_fil.rename(
        columns={
            "NAMA WAJIB PAJAK": "NAMA",
            "KODE MAP": "KDMAP",
            "KODE BAYAR": "KDBAYAR",
            "JUMLAH BAYAR (Rp)": "NOMINAL",
            "NO SK SSP": "NOSK",
            "MASA PAJAK": "MASA",
            "MASA PAJAK2": "MASA2",
            "KODE BANK": "BANK",
            "NO SPM": "NOSPM",
        }
    )
    data_spm_fil["BULANBAYAR"] = data_spm_fil["BULANBAYAR"].astype("int")
    data_spm_fil["SOURCE"] = 2
    data_spm_fil["BILLING"] = ""
    data_spm_fil["NOP"] = ""
    data_spm_fil["PEMBUAT"] = ""
    data_spm_fil["KET"] = ""

    data_spm_fil.columns = [x.lower() for x in data_spm_fil.columns]
    data_spm_fil = data_spm_fil[mpnspm_columns]

    mpnspm = pd.concat([data_mpnall, data_spm_fil], axis=0, ignore_index=True)

    mpnspm["tipe"] = ""
    mpnspm["extra"] = ""

    mpnspm_col = [
        "kdmap",
        "kdbayar",
        "masa",
        "tahun",
        "tanggalbayar",
        "bulanbayar",
        "tahunbayar",
        "nominal",
        "masa2",
    ]
    mpnspm[mpnspm_col] = mpnspm[mpnspm_col].apply(lambda x: pd.to_numeric(x))

    return mpnspm


def etl_spmkp(spmkp_files):
    data_spmkp = pd.DataFrame()
    for file in spmkp_files:
        namefile = namefile = (file.split("_"))[1]
        spmkp_temp = pd.read_csv(
            file,
            parse_dates=["TGL SPMKP"],
            dtype={"NPWP": "str", "KD MAP": "int", "NO SPMKP": "str"},
        )
        spmkp_temp["ADMIN"] = namefile
        data_spmkp = pd.concat([data_spmkp, spmkp_temp], axis=0, ignore_index=True)
    data_spmkp["ADMIN"] = data_spmkp["ADMIN"].str.replace(".csv", "")
    data_spmkp.rename(columns={"TGL SPMKP": "TANGGAL", "KD MAP": "KDMAP"}, inplace=True)
    data_spmkp["KPP"] = data_spmkp["NPWP"].str[10:13]
    data_spmkp["CABANG"] = data_spmkp["NPWP"].str[14:]
    data_spmkp["NPWP"] = data_spmkp["NPWP"].str[:9]
    data_spmkp["BULAN"] = data_spmkp["TANGGAL"].dt.month
    data_spmkp["TAHUN"] = data_spmkp["TANGGAL"].dt.year
    data_spmkp["NOMINAL"] = (
        data_spmkp["NILAI SPMKP"].str.replace(",", "").astype("int64")
    )
    data_spmkp.columns = [x.lower() for x in data_spmkp.columns]
    spmkp_columns = [
        "admin",
        "npwp",
        "kpp",
        "cabang",
        "kdmap",
        "bulan",
        "tahun",
        "tanggal",
        "nominal",
    ]
    data_spmkp = data_spmkp[spmkp_columns]
    return data_spmkp


def etl_pbk(pbk_files):
    data_pbk = pd.DataFrame()
    for file in pbk_files:
        namefile = namefile = (file.split("_"))[1]
        pbk_temp = pd.read_csv(
            file,
            parse_dates=["TGL_DOKUMEN", "TGL_BERLAKU"],
            dtype={
                "NPWP": "str",
                "KPP": "str",
                "CAB": "str",
                "KPPADM_LB": "str",
                "NPWP.1": "str",
                "KPP.1": "str",
                "CAB.1": "str",
                "MAP.1": "str",
                "KD SETOR.1": "str",
                "MAP": "str",
                "MAP.1": "str",
                "KD SETOR": "str",
                "KPPADM_KB": "str",
            },
        )
        pbk_temp["ADMIN"] = namefile
        data_pbk = pd.concat([data_pbk, pbk_temp], axis=0, ignore_index=True)
    data_pbk["JUMLAH_PBK"] = data_pbk["JUMLAH_PBK"].str.replace(",", "")
    data_pbk["JUMLAH_PBK"] = data_pbk["JUMLAH_PBK"].astype("int64")
    data_pbk["TGL_DOKUMEN"] = pd.to_datetime(data_pbk["TGL_DOKUMEN"], format="%Y%m%d")
    data_pbk["TAHUN"] = data_pbk["TGL_DOKUMEN"].dt.year

    data_pbk.rename(
        columns={
            "NOMOR_PBK": "NOPBK",
            "TGL_DOKUMEN": "TANGGALDOC",
            "TGL_BERLAKU": "TANGGALBERLAKU",
            "JUMLAH_PBK": "NOMINAL",
            "CURRENCY_PBK": "CURRENCY",
            "TIPE_PBK": "TIPE",
            "FG_STATUS": "STATUS",
            "NPWP": "NPWP",
            "KPP": "KPP",
            "CAB": "CABANG",
            "NAMA": "NAMA",
            "MAP": "KDMAP",
            "KD SETOR": "KDBAYAR",
            "MASA PAJAK": "MASA_PAJAK",
            "TAHUN PAJAK": "TAHUN_PAJAK",
            "KPPADM_LB": "KPP_ADMIN",
            "NPWP.1": "NPWP2",
            "KPP.1": "KPP2",
            "CAB.1": "CABANG2",
            "NAMA.1": "NAMA2",
            "MAP.1": "KDMAP2",
            "KD SETOR.1": "KDBAYAR2",
            "MASA PAJAK.1": "MASA_PAJAK2",
            "TAHUN PAJAK.1": "TAHUNPAJAK2",
            "KPPADM_KB": "KPP_ADMIN2",
            "NTPN": "NTPN",
            "NO PROD HUKUM": "NO_PROD_HUKUM",
        },
        inplace=True,
    )

    data_pbk = data_pbk.filter(
        [
            "ADMIN",
            "TAHUN",
            "NOPBK",
            "TANGGALDOC",
            "TANGGALBERLAKU",
            "NOMINAL",
            "CURRENCY",
            "TIPE",
            "STATUS",
            "NPWP",
            "KPP",
            "CABANG",
            "NAMA",
            "KDMAP",
            "KDBAYAR",
            "MASA_PAJAK",
            "TAHUN_PAJAK",
            "KPP_ADMIN",
            "NPWP2",
            "KPP2",
            "CABANG2",
            "NAMA2",
            "KDMAP2",
            "KDBAYAR2",
            "MASA_PAJAK2",
            "TAHUN_PAJAK2",
            "KPP_ADMIN2",
            "NTPN",
            "NO_PROD_HUKUM",
        ]
    )

    data_pbk["NO_PROD_HUKUM"].fillna("", inplace=True)
    colmap = {
        "masa_pajak": "masapajak",
        "masa_pajak2": "masapajak2",
        "tahun_pajak": "tahunpajak",
        "tahun_bayar": "tahunbayar",
        "bulan_bayar": "bulanbayar",
    }
    data_pbk.columns = [col.lower() for col in data_pbk.columns]
    data_pbk.rename(columns=colmap, inplace=True)

    data_pbk["tanggalbayar"] = data_pbk["tanggaldoc"].dt.day
    data_pbk["bulanbayar"] = data_pbk["tanggaldoc"].dt.month
    data_pbk["tahunbayar"] = data_pbk["tanggaldoc"].dt.year
    return data_pbk


if __name__ == "__main__":
    kpp = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "097"]

    tahun = "2023"
    jns_pajak = "411100000"
    tgl_awal = "01"
    tgl_akhir = "31"
    bulan = generate_month_list()

    valuta = ["1", "3"]

    login()
    mpn(valuta, kpp, bulan)
    spm(spm_baseUrl, kpp, bulan)

    idr_files = glob.glob(r"downloaded\1\*.csv")
    usd_files = glob.glob(r"downloaded\2\*.csv")
    dolar_file = glob.glob(r"downloaded\2\*.xls")
    pbb_files = glob.glob(r"downloaded\3\*.csv")
    spm_files = glob.glob(r"downloaded\spm\*.csv")
    mpnspm = etl_mpnspm(idr_files, usd_files, dolar_file, pbb_files, spm_files)
    spmkp = etl_spmkp()
