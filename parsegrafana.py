import sqlite3, json

con = sqlite3.connect ("/var/lib/grafana/grafana.db")
cur = con.cursor ()

for row in cur.execute ("SELECT data FROM dashboard WHERE slug=\"tasmota-esps\""):
	# print ("row:", row)
	dashboard = json.loads (row [0])
	# print ("Dashboards:", len (dashboard))
	# print (json.dumps (dashboard, indent=2, sort_keys=True))
	cnt = 0

	for panel in dashboard ["panels"]:
		# print (json.dumps (panel, indent=2, sort_keys=True))
		# print ("panel", cnt, panel.keys ())
		# print ("fieldConfig", cnt, panel ["fieldConfig"].keys ())
		print ("overrides", cnt, panel ["fieldConfig"] ["overrides"])
		cnt += 1

	print ("Panel 4:")
	print (dashboard ["panels"] [4] ["fieldConfig"] ["overrides"] [2])
	print (dashboard ["panels"] [4] ["fieldConfig"] ["overrides"] [2] ["properties"] [0] ["value"])
	dashboard ["panels"] [4] ["fieldConfig"] ["overrides"] [2] ["properties"] [0] ["value"] = "Test Rechteck"
	print (dashboard ["panels"] [4] ["fieldConfig"] ["overrides"] [2] ["properties"] [0] ["value"])

	# print ("OLD:", row)
	# newrow = (json.dumps (dashboard, separators = (",", ":")).encode ("utf-8"), )
	newrow = json.dumps (dashboard, separators = (",", ":")).encode ("utf-8")
	# print ("NEW:", newrow)

	for testrow in cur.execute ("SELECT data FROM dashboard WHERE slug=\"tasmota-esps\" AND data = ?", (row [0], )):
		# print ("testrow:", testrow)
		print ("gefunden")

	con.execute ("UPDATE dashboard SET data = ? WHERE slug=\"tasmota-esps\" AND data = ?", (newrow, row [0]))

	for testrow in cur.execute ("SELECT data FROM dashboard WHERE slug=\"tasmota-esps\""):
		# print ("testrow:", testrow)
		print ("gefunden")

con.commit ()
con.close ()
