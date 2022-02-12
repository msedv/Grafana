# ----------------------------------------------------------------------------
#                    DISPLAY/SHOW FORMATTED GRAFANA SETTING 
#
# python3 showgrafana.py: all dashboards
# python3 showgrafana.py <dashboard-name>: one dashboard
# ----------------------------------------------------------------------------
# (c) 2022-2022 msedv - DI Markus Schwaiger EDV-Dienstleistungen
#               Phone: +43-1-5449532-0; Fax: +43-1-5449532-14
#               Internet: http://www.msedv.at; Mail: office@msedv.at
#               SnailMail: Hauptstr. 110, A-1140 Wien/Vienna, Austria
# ----------------------------------------------------------------------------
#  History:
# 12. 2.2022 MS Initial implementation
# ----------------------------------------------------------------------------
# https://github.com/msedv/Grafana
# https://community.grafana.com/t/lookup-of-device-ids-for-legend/60401
# https://stackoverflow.com/questions/65860003/physical-location-of-grafana-dashboards
# https://docs.python.org/3/library/sqlite3.html
# ----------------------------------------------------------------------------
#  ToDo:
# * Error handling
# ----------------------------------------------------------------------------

import sqlite3, json, csv
from sys import argv

con = sqlite3.connect ("/var/lib/grafana/grafana.db")
cur = con.cursor ()

print (len (argv), argv)

sql = "SELECT slug, data FROM dashboard"

if len (argv) == 2:
	sql += " WHERE slug = \"" + argv [1] + "\""

for row in cur.execute (sql):
	slug = row [0]
	dashboard = json.loads (row [1])

	if len (argv) == 2:
		print ("dashboard:", slug)

	print (json.dumps (dashboard, indent=2, sort_keys=True))

con.close ()
