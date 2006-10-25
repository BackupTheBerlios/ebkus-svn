# coding: latin-1

# Download-Adressen der benötigten Software
#
# create_cd.py und install.py verwenden die hier
# definierten Adressen für den automatischen Download.
#
# Alle downloads kommen jetzt vom ftp-Server der BKE.
# Da sind wir sicher, dass sie auch dort bleiben.

ftp_bke_linux = "ftp://ftp.bke.de/pub/ebkus/ebkus-3.2/linux/"
ftp_bke_win32 = "ftp://ftp.bke.de/pub/ebkus/ebkus-3.2/win32/"

python_win32 = ftp_bke_win32 + 'Python-2.3.4.exe'
python_linux = ftp_bke_linux + 'Python-2.3.4.tgz'

# Original-Quelle ist http://prdownloads.sourceforge.net/mysql-python/MySQL-python-1.0.0.win32-py2.3.zip
mysql_python_win32 = ftp_bke_win32 + 'MySQL-python-1.0.0.win32-py2.3.zip'
mysql_python_linux = ftp_bke_linux + 'MySQL-python-1.0.0.tar.gz'

mysql_win32 = ftp_bke_win32 + 'mysql-4.0.18-win-noinstall.zip'
mysql_linux = ftp_bke_linux + 'mysql-4.0.18.tar.gz'


# Original-Quelle ist http://www.nullcube.com/software/pygdchart/, jedoch meistens sehr langsam
pygdchart_win32 = ftp_bke_win32 + 'pygdchart0.6.1-w32-py23.zip'
pygdchart_linux = ftp_bke_linux + 'pygdchart0.6.1-linux-py23.zip'

# Original-Quelle ist http://tor.ath.cx/~hunter/apache/, jedoch meistens sehr langsam
openssl_win32 = ftp_bke_win32 + 'Openssl-0.9.7d-Win32.zip'
openssl_linux = ftp_bke_linux + 'openssl-0.9.7d.tar.gz'

modssl_linux = ftp_bke_linux + 'mod_ssl-2.8.18-1.3.31.tar.gz'

# Original-Quelle ist http://tor.ath.cx/~hunter/apache/, jedoch meistens sehr langsam
apache_win32 = ftp_bke_win32 + 'Apache_1.3.31-Mod_SSL_2.8.17-Openssl_0.9.7d-Win32.zip'
apache_linux = ftp_bke_linux + 'apache_1.3.31.tar.gz'

srvstart_win32 = ftp_bke_win32 + 'srvstart_run.v110.zip'

reportlab = ftp_bke_linux + 'ReportLab_1_19.zip'
