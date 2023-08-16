from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import pandas as pd
from export_sql import export_postgres
from dotenv import load_dotenv

load_dotenv()
lokal_mysql_username = os.getenv("LOCAL_MYSQL_USERNAME")
lokal_mysql_password = os.getenv("LOCAL_MYSQL_PASSWORD")
lokal_mysql_host = os.getenv("LOCAL_MYSQL_HOST")
lokal_mysql_con = create_engine(
    f"mysql://{lokal_mysql_username}:{lokal_mysql_password}@{lokal_mysql_host}/mpninfo"
)

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_con = create_engine(
    f"mysql://{mysql_username}:{mysql_password}@{mysql_host}/mpninfo"
)

postgres_username = os.getenv("POSTGRES_USERNAME")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_password_parse = quote_plus(postgres_password)
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database = os.getenv("POSTGRES_DB")
postgre_con = create_engine(
    f"postgresql://{postgres_username}:{postgres_password_parse}@{postgres_host}/{postgres_database}"
)

kueri_union = """
SELECT admin,
    npwp,
    kpp,
    cabang,
    nama,
    kdmap,
    kdbayar,
    masa,
    masa2,
    tahun,
    tanggalbayar,
    bulanbayar,
    tahunbayar,
    datebayar,
    nominal,
    ntpn,
    bank,
    nosk,
    nospm,
    tipe,
    source,
    extra,
    billing,
    nop,
    pembuat,
    CASE WHEN SOURCE = 1 THEN 'MPN' ELSE 'SPM' END AS ket 
    FROM MPN WHERE TAHUNBAYAR =2023
    UNION ALL 
    SELECT admin,
    npwp,
    kpp,
    cabang,
    '',
    kdmap,
    '',
    '',
    '',
    '',
    DAY(tanggal) AS TANGGALBAYAR,
    BULAN,
    TAHUN,
    tanggal,
    NOMINAL*-1,
    '',
    '',
    '',
    '',
    '',
    3 AS SOURCE,
    '',
    '',
    '',
    '',
    'SPMKP' AS 'ket' 
    FROM spmkp WHERE TAHUN=2023
    UNION ALL 
    SELECT A.admin,
    A.npwp,
    A.kpp,
    A.cabang,
    A.nama,
    kdmap,
    kdbayar,
    masapajak,
    masapajak,
    tahunpajak,
    DAY(TANGGALDOC) AS TANGGALBAYAR,
    MONTH(TANGGALDOC) BULAN,
    YEAR(TANGGALDOC) TAHUN,
    TANGGALDOC,
    NOMINAL*-1 as "NOMINAL",
    ntpn,
    '',
    nopbk,
    '',
    '',
    4 AS SOURCE,
    '',
    '',
    '',
    '',
    'PBK KIRIM' AS ket 
    FROM PBK A 
    WHERE admin = kpp_admin AND kpp_admin = admin and YEAR(TANGGALDOC)=2023
    UNION ALL 
    SELECT A.ADMIN,
    npwp2,
    kpp2,
    cabang2,
    nama2,
    kdmap2,
    kdbayar2,
    masapajak2,
    masapajak2,
    tahunpajak2,
    DAY(TANGGALDOC) AS TANGGALBAYAR,
    MONTH(TANGGALDOC) BULAN,
    YEAR(TANGGALDOC) TAHUN,
    TANGGALDOC,
    NOMINAL,
    ntpn,
    '',
    nopbk,
    '',
    '',
    5 AS SOURCE,
    '',
    '',
    '',
    '',
    'PBK TERIMA' AS ket 
    FROM PBK A 
    WHERE admin = kpp_admin2 AND kpp_admin2 = admin and YEAR(TANGGALDOC)=2023
"""

union = pd.read_sql(kueri_union, con=lokal_mysql_con)
union["NPWP15"] = union["npwp"] + union["kpp"] + union["cabang"]

data_sektor = pd.read_sql(
    """ SELECT
	m.NPWP15,
    m.NAMA_WP,
	m.NAMA_AR ,
	m.SEKSI ,
	m.SEGMENTASI_WP ,
	m.JENIS_WP,
	m.KODE_KLU ,
	m.NAMA_KLU ,
	dk.KD_KATEGORI ,
	dk.NM_KATEGORI ,
	dk.KD_GOLPOK ,
	dk.NM_GOLPOK
FROM
	registrasi.sidjp_masterfile m
LEFT JOIN dimensi.dim_klu dk ON
	m.KODE_KLU = dk.KD_KLU""",
    con=mysql_con,
)

kdmap = pd.read_sql(
    """ 
    select "KDMAP","KDBAYAR","URAIAN","MAP" from dimensi.map_lengkap""",
    con=postgre_con,
)
data = union.merge(data_sektor, on="NPWP15", how="left")
data = data.merge(
    kdmap, left_on=["kdmap", "kdbayar"], right_on=["KDMAP", "KDBAYAR"], how="left"
)
data.drop(columns=["KDMAP", "KDBAYAR"], inplace=True)
col_toint = [
    "tahun",
]
data[col_toint] = data[col_toint].apply(lambda x: pd.to_numeric(x, downcast="integer"))

# ADJUSTMENT SESUAIKAN ppmpkm2023
# -uppercase columns
data.columns = [x.upper() for x in data.columns]
# nama

# urutkan kolom
ppmpkm_kolom = [
    "ADMIN",
    "NAMA_WP",
    "KDMAP",
    "KDBAYAR",
    "MASA",
    "MASA2",
    "TAHUN",
    "TANGGALBAYAR",
    "BULANBAYAR",
    "TAHUNBAYAR",
    "DATEBAYAR",
    "NOMINAL",
    "NTPN",
    "BANK",
    "NOSK",
    "NOSPM",
    "KET",
    "NPWP15",
    "NAMA_AR",
    "SEKSI",
    "SEGMENTASI_WP",
    "JENIS_WP",
    "KODE_KLU",
    "NAMA_KLU",
    "KD_KATEGORI",
    "NM_KATEGORI",
    "KD_GOLPOK",
    "NM_GOLPOK",
    "URAIAN",
    "MAP",
]
data = data[ppmpkm_kolom]

# DELETE TAHUN 2023 DLUU
# Create a connection to the database
import psycopg2

print(postgres_host, postgres_username, postgres_password_parse, postgres_database)
connection = psycopg2.connect(
    host=postgres_host,
    user=postgres_username,
    password="kwl@110",
    database=postgres_database,
)
cursor = connection.cursor()

delete_query = 'DELETE FROM ppmpkm WHERE "TAHUNBAYAR"=2023 '
cursor.execute(delete_query)
connection.commit()
print(f"{cursor.rowcount} row(s) deleted.")

data.to_sql("ppmpkm", con=postgre_con, index=False, if_exists="append")

# export_postgres(data, "penerimaan2023")
