from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
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

union = pd.read_sql(kueri_union, con=mysql_con)
union["NPWP15"] = union["npwp"] + union["kpp"] + union["cabang"]

data_sektor = pd.read_sql(
    """ SELECT
	m.NPWP15,
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
    select "KDMAP","MAP" from dimensi.map_polos""",
    con=postgre_con,
)
data = union.merge(data_sektor, on="NPWP15", how="left")
data = data.merge(kdmap, left_on="kdmap", right_on="KDMAP", how="outer")
print(union.head())
