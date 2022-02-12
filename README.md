# Grafana

Collection of scripts regarding automatization of Grafana-tasks

# Changing legends with Python

The initial discussion: https://community.grafana.com/t/lookup-of-device-ids-for-legend/60401

Where is Grafana data stored: https://stackoverflow.com/questions/65860003/physical-location-of-grafana-dashboards

* the configuration of the dashboards etc. can usually be found in /var/lib/grafana/grafana.db
* which is a sqlite-Database with only one entry per dashboard
* the "real" definitions are JSON-encoded in the "data" field of the dashboard-table
* where there's an element "overrides" which is what we need

To get an overview of the data: https://sqlitebrowser.org/

To change it with SQL from the BASH: https://sqlite.org/cli.html

```
apt install sqlite3
sqlite3 /var/lib/grafana/grafana.db
.tables
SELECT data FROM dashboard;
.exit
```

But: additional parsing of the JSON-data is needed. Python supports sqlite __and__ JSON de-/encoding thus I built the POC (proof of concept) https://github.com/msedv/Grafana/blob/main/parsegrafana.py.

sqlite-access from Python: https://docs.python.org/3/library/sqlite3.html
