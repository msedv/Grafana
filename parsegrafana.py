# ----------------------------------------------------------------------------
#                    PARSING AND CHANGING GRAFANA SETTING 
# ----------------------------------------------------------------------------
# (c) 2022-2022 msedv - DI Markus Schwaiger EDV-Dienstleistungen
#               Phone: +43-1-5449532-0; Fax: +43-1-5449532-14
#               Internet: http://www.msedv.at; Mail: office@msedv.at
#               SnailMail: Hauptstr. 110, A-1140 Wien/Vienna, Austria
# ----------------------------------------------------------------------------
#  History:
# 10. 2.2022 MS Proof of concept
# 12. 2.2022 MS Field translation
# 13. 2.2022 MS Handling of alias/target
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

con = sqlite3.connect ("/var/lib/grafana/grafana.db")
cur = con.cursor ()

for row in cur.execute ("SELECT slug, data FROM dashboard"):
	slug = row [0]
	# print ("slug", slug)
	dashboard = json.loads (row [1])
	# print ("title", dashboard ["title"])
	# print (json.dumps (dashboard, indent=2, sort_keys=True))

	with open ("parsegrafana.csv", newline="") as csvfile:
		reader = csv.DictReader (csvfile)

		for mapLine in reader:
										# mapLine = {'dashboard': 'tasmota-esps', 'panel': '*', 'from': 'TASMOTA_5F101D', 'to': 'Werkstatt'}
			# print (mapLine)

			if (mapLine ["dashboard"] == "*") or (mapLine ["dashboard"] == slug):
				for panelIndex in range (len (dashboard ["panels"])):
					# print (json.dumps (dashboard ["panels"] [panelIndex], indent=2, sort_keys=True))
					# print ("panel", dashboard ["panels"] [panelIndex].keys ())
					# print ("fieldConfig", dashboard ["panels"] [panelIndex] ["fieldConfig"].keys ())
					# print ("title", dashboard ["panels"] [panelIndex] ["title"])
					# print ("fieldConfig", json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"], indent=2, sort_keys=True))

					if (mapLine ["panel"] == "*") or (dashboard ["panels"] [panelIndex] ["title"] == mapLine ["panel"]):
											# [{'matcher': {'id': 'byName', 'options': 'TASMOTA_5F101D'}, 'properties': [{'id': 'displayName', 'value': 'Werkstatt'}]}]
						# print ("fieldConfig", json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"], indent=2, sort_keys=True))
						# print ("overrides", len (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"]), dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"])

						for targetsIndex in range (len (dashboard ["panels"] [panelIndex] ["targets"])):
							# print (dashboard ["panels"] [panelIndex] ["targets"] [targetsIndex] ["alias"])
							replaceFrom = dashboard ["panels"] [panelIndex] ["targets"] [targetsIndex] ["alias"].replace ("$tag_device", mapLine ["from"])
							replaceTo   = dashboard ["panels"] [panelIndex] ["targets"] [targetsIndex] ["alias"].replace ("$tag_device", mapLine ["to"])

							foundOverride = False

							for overrideIndex in range (len (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"])):
								# print ("matcher", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"])
								foundProperties = False

												# We also replace parts of "from"
								if dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].find (replaceFrom) >= 0:
									for propertyIndex in range (len (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"])):
										# print ("property", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex])
					
										if "id" in dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] and \
											 (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] ["id"] == "displayName"):
											if "value" in dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex]:
												if dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] ["value"] == dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo):
													print ("Already done:", dashboard ["title"], "/", dashboard ["panels"] [panelIndex] ["title"],
																 "from", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"],
																 "to",   dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo))
												else:
													print ("Changing:", dashboard ["title"], "/", dashboard ["panels"] [panelIndex] ["title"],
																 "from",         dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"],
																 "to",           dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo),
																 "- old value:", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] ["value"])
													# print (json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"], indent=2, sort_keys=True))
													dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] ["value"] = dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo)
													# print (json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"], indent=2, sort_keys=True))
											else:
												# id "displayName" but no value
												print ("Adding 1:", dashboard ["title"], "/", dashboard ["panels"] [panelIndex] ["title"],
															 "from", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"],
															 "to",   dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo))
												# print (json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"], indent=2, sort_keys=True))
												dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"] [propertyIndex] ["value"] = dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo)
												# print (json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"], indent=2, sort_keys=True))

											foundProperties = True
											foundOverride = True

												# We have overrides but no property for the displayName
									if not (foundProperties):
										# print (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"])
										# print (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo))
										print ("Adding 2:", dashboard ["title"], "/", dashboard ["panels"] [panelIndex] ["title"],
													 "from", dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"],
													 "to",   dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo))
										dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["properties"].append ({"id": "displayName", "value": dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"] [overrideIndex] ["matcher"] ["options"].replace (replaceFrom, replaceTo)})
										foundOverride = True

												# No override for this field
							if not (foundOverride):
								print ("Adding 3:", dashboard ["title"], "/", dashboard ["panels"] [panelIndex] ["title"],
											 "from", replaceFrom,
											 "to",   replaceTo)
								toAdd = {"matcher": {"id": "byName", "options": replaceFrom}, "properties": [{"id": "displayName", "value": replaceTo}]}
								# print (toAdd)
								dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"].append (toAdd)

					# print (json.dumps (dashboard ["panels"] [panelIndex] ["fieldConfig"] ["overrides"], indent=2, sort_keys=True))

		# print ("OLD:", row [1])
		# newrow = (json.dumps (dashboard, separators = (",", ":")).encode ("utf-8"), )
		newrow = json.dumps (dashboard, separators = (",", ":")).encode ("utf-8")
		# print ("NEW:", newrow)

		con.execute ("UPDATE dashboard SET data = ? WHERE slug=\"tasmota-esps\" AND data = ?", (newrow, row [1]))
		con.commit ()

con.close ()
