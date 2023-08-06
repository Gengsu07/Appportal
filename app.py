from mpnspm import login, mpn, spm, etl_mpnspm, generate_month_list, etl_spmkp, etl_pbk
from spmkp import spmkp
from pbk import pbk
from export_sql import export_postgres, export_mysql
import glob
import datetime


username = "810202558"
password = "Gengsu!sh3r3"
# password = os.environ.get("PASSWORD")

today = datetime.date.today()
# download_path = r"C:\Users\810202558\Downloads"
download_path = r"C:\Users\sugengw07\Downloads"
# baseDownloadedDir = r"D:\PROJECTS\Appportal\downloaded"
baseDownloadedDir = r"D:\PROJECTS\Appportal\downloaded"
baseUrl = "https://appportal.intranet.pajak.go.id/portal/download/lsnfjkasbnfjnasjkfnjbnjnjknbkjnfjknbjkfnbkjfnbi3939489184.php?p1="
# kpp = ['001']
spm_baseUrl = "https://appportal.intranet.pajak.go.id/portal/spm/dataspmcsv.php?"
kpp = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "097"]

# kpp = ["001"]
tahun = "2023"
jns_pajak = "411100000"
tgl_awal = "01"
tgl_akhir = "31"
bulan = generate_month_list()
# bulan = ["01"]
valuta = ["1", "3"]

# DownloAD Data
idr_files = glob.glob(r"downloaded\1\*.csv")
usd_files = glob.glob(r"downloaded\2\*.csv")
dolar_file = glob.glob(r"downloaded\2\*.xls")
pbb_files = glob.glob(r"downloaded\3\*.csv")
spm_files = glob.glob(r"downloaded\spm\*.csv")
spmkp_files = glob.glob(r"downloaded\spmkp\*.csv")
pbk_files = glob.glob(r"downloaded\pbk\*.csv")

# login()
# mpn(valuta, kpp, bulan, tahun, jns_pajak, tgl_awal, tgl_akhir)
# spm(spm_baseUrl, kpp, bulan, tgl_awal, tgl_akhir, tahun)
data_mpnspm = etl_mpnspm(idr_files, usd_files, dolar_file, pbb_files, spm_files)
export_mysql(data_mpnspm, "mpn")


# pbk(kpp, download_path, baseDownloadedDir)
# spmkp(kpp, download_path, baseDownloadedDir)
spmkp = etl_spmkp(spmkp_files)
export_mysql(spmkp, "spmkp")
pbk = etl_pbk(pbk_files)
export_mysql(pbk, "pbk")
